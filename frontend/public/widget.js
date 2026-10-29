(function() {
    // 1. Resolve configuration from script data-attributes
    const currentScript = (() => {
        if (document.currentScript) return document.currentScript;
        const scripts = document.getElementsByTagName('script');
        for (let i = 0; i < scripts.length; i++) {
            if (scripts[i].src && (scripts[i].src.includes('widget.js') || scripts[i].getAttribute('data-chatbot-id'))) {
                return scripts[i];
            }
        }
        return scripts[scripts.length - 1];
    })();

    const scriptOrigin = (() => {
        try {
            if (currentScript && currentScript.src) {
                const parsed = new URL(currentScript.src);
                return parsed.origin;
            }
        } catch (e) {}
        return 'https://docagent-ai-production-f51e.up.railway.app';
    })();

    const apiUrl = (currentScript.getAttribute('data-api-url') || scriptOrigin || 'https://docagent-ai-production-f51e.up.railway.app').replace(/\/$/, '');
    const chatbotId = currentScript.getAttribute('data-chatbot-id') || 'default';
    const botName = currentScript.getAttribute('data-bot-name') || 'DocAgent AI';
    const themeColor = currentScript.getAttribute('data-color') || '#D946EF';
    const greetingMsg = currentScript.getAttribute('data-greeting') || 'Hello! How can I help you with our company policies today?';
    let launcherImage = (currentScript.getAttribute('data-launcher-image') || '').trim();

    // State
    const state = {
        chatHistory: [],
        isOpen: false,
        isTyping: false,
        hasGreeted: false
    };

    // Helper to escape HTML to prevent XSS
    function escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Helper to format basic markdown (headers, bold, italic, code, lists, tables)
    function formatMarkdown(text) {
        if (!text) return '';
        let html = escapeHtml(text);

        // Headers: ### Header
        html = html.replace(/^### (.*?)$/gm, '<h4 style="margin: 8px 0 4px 0; font-size: 14px; font-weight: 700; color: #0F172A;">$1</h4>');
        html = html.replace(/^## (.*?)$/gm, '<h3 style="margin: 10px 0 6px 0; font-size: 15px; font-weight: 700; color: #0F172A;">$1</h3>');
        html = html.replace(/^# (.*?)$/gm, '<h2 style="margin: 12px 0 8px 0; font-size: 16px; font-weight: 800; color: #0F172A;">$1</h2>');

        // Bold: **text** -> <strong>text</strong>
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Italics: *text* or _text_ -> <em>text</em>
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        html = html.replace(/_(.*?)_/g, '<em>$1</em>');

        // Inline Code: `code` -> <code>code</code>
        html = html.replace(/`(.*?)`/g, '<code class="docagent-inline-code">$1</code>');

        // Bullet lists
        html = html.replace(/^-\s+(.*)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');

        // Numbered lists
        html = html.replace(/^\d+\.\s+(.*)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*?<\/li>)+/gs, '<ol>$&</ol>');

        // Paragraphs
        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');

        if (!html.startsWith('<p>') && !html.startsWith('<h') && !html.startsWith('<ul>') && !html.startsWith('<ol>')) {
            html = '<p>' + html + '</p>';
        }
        return html;
    }

    // Hex to RGBA utility for glow/shadow effects
    function hexToRgbA(hex, alpha) {
        let c;
        if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)) {
            c = hex.substring(1).split('');
            if (c.length === 3) {
                c = [c[0], c[0], c[1], c[1], c[2], c[2]];
            }
            c = '0x' + c.join('');
            return `rgba(${[(c >> 16) & 255, (c >> 8) & 255, c & 255].join(',')},${alpha})`;
        }
        return `rgba(65, 128, 139, ${alpha})`;
    }

    const glowColor = hexToRgbA(themeColor, 0.35);
    const lightBgColor = hexToRgbA(themeColor, 0.08);

    // 2. Inject Styles with expanded width, height, and modern clear aesthetic
    const styleTag = document.createElement('style');
    styleTag.innerHTML = `
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap');

        /* Main Container */
        .docagent-widget-container {
            font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 2147483647;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            pointer-events: none !important;
        }

        /* Floating Launcher Button */
        .docagent-widget-launcher {
            box-sizing: border-box;
            padding: 4px;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, ${themeColor} 0%, rgba(30, 90, 100, 0.95) 100%);
            box-shadow: 0 10px 28px ${glowColor}, 0 2px 10px rgba(0,0,0,0.12);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid rgba(255, 255, 255, 0.25);
            outline: none;
            pointer-events: auto !important;
        }

        .docagent-widget-launcher:hover {
            transform: scale(1.08) translateY(-2px);
            box-shadow: 0 14px 34px ${glowColor}, 0 4px 14px rgba(0,0,0,0.18);
        }

        .docagent-widget-launcher:active {
            transform: scale(0.95);
        }

        .docagent-widget-launcher svg {
            width: 30px;
            height: 30px;
            fill: #ffffff;
            transition: transform 0.3s ease;
        }

        .docagent-widget-launcher img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
            display: block;
        }

        .docagent-widget-launcher.open svg {
            transform: rotate(90deg);
        }

        /* Chat Panel/Window - Wide, Long, & Clear */
        .docagent-widget-panel {
            width: 460px;
            height: 660px;
            max-height: calc(100vh - 110px);
            max-width: calc(100vw - 32px);
            background: #FFFFFF;
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 24px;
            box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18), 0 4px 16px rgba(15, 23, 42, 0.06);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            margin-bottom: 16px;
            opacity: 0;
            visibility: hidden;
            pointer-events: none !important;
            transform: translateY(20px) scale(0.96);
            transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                        transform 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                        visibility 0.25s;
            transform-origin: bottom right;
        }

        .docagent-widget-panel.open {
            opacity: 1;
            visibility: visible;
            pointer-events: auto !important;
            transform: translateY(0) scale(1);
        }

        .docagent-widget-panel.closed {
            display: none !important;
        }

        /* Header */
        .docagent-widget-header {
            background: linear-gradient(135deg, ${themeColor} 0%, rgba(30, 90, 100, 0.95) 100%);
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: #ffffff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            border-bottom: 1px solid rgba(255,255,255,0.12);
            flex-shrink: 0;
        }

        .docagent-widget-header-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .docagent-widget-header-avatar {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1.5px solid rgba(255,255,255,0.3);
            flex-shrink: 0;
        }

        .docagent-widget-header-avatar svg {
            width: 22px;
            height: 22px;
            fill: #ffffff;
        }

        .docagent-widget-header-details {
            display: flex;
            flex-direction: column;
        }

        .docagent-widget-header-name {
            font-size: 16px;
            font-weight: 700;
            letter-spacing: -0.2px;
            margin: 0;
            line-height: 1.2;
        }

        .docagent-widget-header-status {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 3px;
        }

        .docagent-widget-header-dot {
            width: 7px;
            height: 7px;
            background: #7FB800; /* vibrant lime green */
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 6px #7FB800;
        }

        .docagent-widget-header-close {
            background: rgba(255, 255, 255, 0.15);
            border: none;
            cursor: pointer;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 10px;
            transition: all 0.2s;
        }

        .docagent-widget-header-close:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }

        .docagent-widget-header-close svg {
            width: 18px;
            height: 18px;
            fill: currentColor;
        }

        /* Message List / Chat Body */
        .docagent-widget-chat-history {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 14px;
            background-color: #F8FAFC;
        }

        /* Clean Scrollbar */
        .docagent-widget-chat-history::-webkit-scrollbar {
            width: 6px;
        }
        .docagent-widget-chat-history::-webkit-scrollbar-track {
            background: transparent;
        }
        .docagent-widget-chat-history::-webkit-scrollbar-thumb {
            background: rgba(15, 23, 42, 0.12);
            border-radius: 10px;
        }
        .docagent-widget-chat-history::-webkit-scrollbar-thumb:hover {
            background: rgba(15, 23, 42, 0.22);
        }

        /* Message bubble structure */
        .docagent-widget-msg {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            max-width: 88%;
        }

        .docagent-widget-msg-user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .docagent-widget-msg-agent {
            align-self: flex-start;
        }

        .docagent-widget-msg-avatar {
            width: 32px;
            height: 32px;
            border-radius: 10px;
            background: ${lightBgColor};
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            border: 1px solid rgba(65, 128, 139, 0.2);
            margin-top: 2px;
        }

        .docagent-widget-msg-avatar svg {
            width: 18px;
            height: 18px;
            fill: ${themeColor};
        }

        .docagent-widget-msg-user .docagent-widget-msg-avatar {
            background: #E2E8F0;
            border-color: #CBD5E1;
        }

        .docagent-widget-msg-user .docagent-widget-msg-avatar svg {
            fill: #475569;
        }

        .docagent-widget-msg-bubble {
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.6;
            color: #0F172A;
            word-break: break-word;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        .docagent-widget-msg-user .docagent-widget-msg-bubble {
            background: ${themeColor};
            color: #ffffff;
            border-bottom-right-radius: 4px;
            box-shadow: 0 4px 14px ${glowColor};
        }

        .docagent-widget-msg-agent .docagent-widget-msg-bubble {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-bottom-left-radius: 4px;
        }

        /* Markdown styling inside bubbles */
        .docagent-widget-msg-bubble p {
            margin: 0 0 8px 0;
        }
        .docagent-widget-msg-bubble p:last-child {
            margin-bottom: 0;
        }
        .docagent-widget-msg-bubble strong {
            color: #0F172A;
            font-weight: 700;
        }
        .docagent-widget-msg-user .docagent-widget-msg-bubble strong {
            color: #ffffff;
        }
        .docagent-inline-code {
            background: #FFF1EE;
            color: #F46036;
            border: 1px solid #FFD8CE;
            padding: 2px 6px;
            border-radius: 5px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 12.5px;
            font-weight: 600;
        }
        .docagent-widget-msg-user .docagent-inline-code {
            background: rgba(255, 255, 255, 0.2);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.3);
        }
        .docagent-widget-msg-bubble ul, .docagent-widget-msg-bubble ol {
            margin: 6px 0 10px 20px;
            padding: 0;
        }
        .docagent-widget-msg-bubble li {
            margin-bottom: 5px;
        }

        /* Sources Card */
        .docagent-widget-sources {
            margin-top: 10px;
            border-top: 1px solid #E2E8F0;
            padding-top: 8px;
        }

        .docagent-widget-sources-btn {
            background: none;
            border: none;
            color: ${themeColor};
            font-size: 11.5px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 0;
            font-weight: 700;
            transition: color 0.2s;
        }

        .docagent-widget-sources-btn:hover {
            color: #0F172A;
        }

        .docagent-widget-sources-btn svg {
            width: 14px;
            height: 14px;
            fill: currentColor;
            transition: transform 0.2s;
        }

        .docagent-widget-sources-btn.active svg {
            transform: rotate(180deg);
        }

        .docagent-widget-sources-content {
            display: none;
            flex-direction: column;
            gap: 8px;
            margin-top: 8px;
        }

        .docagent-widget-source-item {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 11px;
        }

        .docagent-widget-source-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 4px;
            gap: 6px;
        }

        .docagent-widget-source-title {
            font-weight: 700;
            color: #1E293B;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .docagent-widget-source-badge {
            font-size: 10px;
            font-weight: 700;
            color: #15803D;
            background: #DCFCE7;
            padding: 1px 6px;
            border-radius: 6px;
            flex-shrink: 0;
        }

        .docagent-widget-source-text {
            color: #475569;
            margin: 0;
            font-style: italic;
            line-height: 1.4;
        }

        /* Typing indicator */
        .docagent-widget-typing {
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 4px 8px;
        }

        .docagent-widget-typing-dot {
            width: 7px;
            height: 7px;
            background: ${themeColor};
            border-radius: 50%;
            animation: docagent-typing 1.4s infinite both;
        }

        .docagent-widget-typing-dot:nth-child(1) { animation-delay: 0s; }
        .docagent-widget-typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .docagent-widget-typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes docagent-typing {
            0%, 80%, 100% { transform: scale(0.6); opacity: 0.35; }
            40% { transform: scale(1); opacity: 1; }
        }

        /* Footer Input Area */
        .docagent-widget-footer {
            padding: 14px 18px;
            background: #FFFFFF;
            border-top: 1px solid #E2E8F0;
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex-shrink: 0;
        }

        .docagent-widget-input-row {
            display: flex;
            align-items: center;
            background: #F8FAFC;
            border: 1.5px solid #E2E8F0;
            border-radius: 16px;
            padding: 4px 6px 4px 14px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .docagent-widget-input-row:focus-within {
            border-color: ${themeColor};
            box-shadow: 0 0 0 3px ${glowColor};
            background: #FFFFFF;
        }

        .docagent-widget-input,
        .docagent-widget-input:focus,
        .docagent-widget-input:focus-visible,
        .docagent-widget-input:active,
        .docagent-widget-input:hover {
            flex: 1;
            background: transparent !important;
            border: none !important;
            border-width: 0 !important;
            border-style: none !important;
            border-color: transparent !important;
            outline: none !important;
            outline-width: 0 !important;
            outline-style: none !important;
            outline-color: transparent !important;
            box-shadow: none !important;
            -webkit-box-shadow: none !important;
            -moz-box-shadow: none !important;
            --tw-ring-shadow: 0 0 #0000 !important;
            --tw-ring-offset-shadow: 0 0 #0000 !important;
            --tw-shadow: 0 0 #0000 !important;
            --tw-ring-color: transparent !important;
            appearance: none !important;
            -webkit-appearance: none !important;
            -moz-appearance: none !important;
            color: #0F172A !important;
            font-size: 14px !important;
            padding: 8px 0 !important;
            resize: none !important;
            font-family: inherit !important;
            max-height: 90px !important;
            line-height: 1.4 !important;
        }

        .docagent-widget-input::placeholder {
            color: #94A3B8 !important;
        }

        .docagent-widget-send-btn {
            background: ${themeColor};
            border: none;
            width: 38px;
            height: 38px;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            transition: all 0.2s;
            flex-shrink: 0;
            box-shadow: 0 2px 8px ${glowColor};
        }

        .docagent-widget-send-btn:hover:not(:disabled) {
            transform: scale(1.05);
            background: ${themeColor};
            filter: brightness(1.08);
        }

        .docagent-widget-send-btn:disabled {
            background: #E2E8F0;
            color: #94A3B8;
            box-shadow: none;
            cursor: not-allowed;
        }

        .docagent-widget-send-btn svg {
            width: 16px;
            height: 16px;
            fill: currentColor;
        }

        .docagent-widget-brand-link {
            font-size: 11px;
            color: #64748B;
            text-align: center;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            font-weight: 500;
        }
        
        .docagent-widget-brand-link:hover {
            color: ${themeColor};
        }

        .docagent-widget-brand-link svg {
            width: 11px;
            height: 11px;
            fill: currentColor;
        }

        /* Pill Action Button above chat input */
        .docagent-widget-pill-bar {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding: 0 2px 2px 2px;
        }

        .docagent-widget-pill-btn {
            background: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 9999px;
            padding: 5px 13px;
            font-size: 11.5px;
            font-weight: 700;
            color: #334155;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            font-family: inherit;
        }

        .docagent-widget-pill-btn:hover {
            background: ${themeColor};
            color: #FFFFFF;
            border-color: ${themeColor};
            transform: translateY(-1px);
            box-shadow: 0 4px 12px ${glowColor};
        }

        .docagent-widget-pill-btn:active {
            transform: translateY(0) scale(0.98);
        }

        .docagent-widget-pill-btn svg {
            width: 13px;
            height: 13px;
            fill: currentColor;
            transition: transform 0.2s;
        }

        .docagent-widget-pill-btn:hover svg {
            transform: scale(1.15);
        }

        /* Inquiry View Interface (Direct Admin Contact Form) */
        .docagent-widget-inquiry-view {
            flex: 1;
            padding: 18px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background-color: #F8FAFC;
        }

        .docagent-widget-inquiry-header {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 14px 16px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
        }

        .docagent-widget-inquiry-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: ${themeColor};
            background: ${lightBgColor};
            padding: 3px 8px;
            border-radius: 6px;
            margin-bottom: 6px;
        }

        .docagent-widget-inquiry-badge svg {
            width: 12px;
            height: 12px;
            fill: currentColor;
        }

        .docagent-widget-inquiry-title {
            font-size: 15px;
            font-weight: 800;
            color: #0F172A;
            margin: 0 0 4px 0;
            line-height: 1.25;
        }

        .docagent-widget-inquiry-desc {
            font-size: 11.5px;
            color: #64748B;
            margin: 0;
            line-height: 1.5;
        }

        .docagent-widget-form-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
        }

        .docagent-widget-form-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .docagent-widget-form-label {
            font-size: 11px;
            font-weight: 700;
            color: #334155;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .docagent-widget-form-input, .docagent-widget-form-textarea {
            background: #F8FAFC;
            border: 1.5px solid #E2E8F0;
            border-radius: 12px;
            padding: 9px 12px;
            font-size: 13px;
            color: #0F172A;
            outline: none;
            font-family: inherit;
            transition: all 0.2s;
            box-sizing: border-box;
            width: 100%;
        }

        .docagent-widget-form-input:focus, .docagent-widget-form-textarea:focus {
            background: #FFFFFF;
            border-color: ${themeColor};
            box-shadow: 0 0 0 3px ${glowColor};
        }

        .docagent-widget-form-textarea {
            resize: vertical;
            min-height: 85px;
            line-height: 1.4;
        }

        .docagent-widget-form-error {
            background: #FEF2F2;
            border: 1px solid #FECACA;
            color: #DC2626;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            display: none;
            align-items: center;
            gap: 6px;
        }

        .docagent-widget-form-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 8px;
            margin-top: 4px;
        }

        .docagent-widget-form-cancel {
            background: transparent;
            border: 1px solid #CBD5E1;
            color: #475569;
            border-radius: 12px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .docagent-widget-form-cancel:hover {
            background: #F1F5F9;
            color: #0F172A;
        }

        .docagent-widget-form-submit {
            background: ${themeColor};
            border: none;
            color: #FFFFFF;
            border-radius: 12px;
            padding: 8px 18px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            box-shadow: 0 2px 8px ${glowColor};
            font-family: inherit;
        }

        .docagent-widget-form-submit:hover:not(:disabled) {
            filter: brightness(1.08);
            transform: translateY(-1px);
        }

        .docagent-widget-form-submit:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .docagent-widget-form-submit svg {
            width: 14px;
            height: 14px;
            fill: currentColor;
        }

        /* Mobile viewport responsiveness */
        @media (max-width: 640px) {
            .docagent-widget-container {
                bottom: 12px;
                right: 12px;
                pointer-events: none !important;
            }
            .docagent-widget-panel {
                width: calc(100vw - 24px);
                height: calc(100vh - 90px);
                max-width: calc(100vw - 24px);
                max-height: calc(100vh - 90px);
                margin-bottom: 12px;
                border-radius: 20px;
            }
            .docagent-widget-launcher {
                width: 56px;
                height: 56px;
                pointer-events: auto !important;
            }
        }
    `;
    document.head.appendChild(styleTag);

    // 3. SVG Constants
    const SVGS = {
        robot: `<svg viewBox="0 0 24 24"><path d="M12 2A2 2 0 0 1 14 4V5.07A8 8 0 0 1 21 13V15A3 3 0 0 1 18 18H17.82A6 6 0 0 1 16 21H14A2 2 0 0 1 12 19A2 2 0 0 1 10 21H8A6 6 0 0 1 6.18 18H6A3 3 0 0 1 3 15V13A8 8 0 0 1 10 5.07V4A2 2 0 0 1 12 2M12 7A6 6 0 0 0 6 13V15A1 1 0 0 0 7 16H17A1 1 0 0 0 18 15V13A6 6 0 0 0 12 7M9 10A1.5 1.5 0 1 1 7.5 11.5A1.5 1.5 0 0 1 9 10M15 10A1.5 1.5 0 1 1 13.5 11.5A1.5 1.5 0 0 1 15 10Z"/></svg>`,
        user: `<svg viewBox="0 0 24 24"><path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/></svg>`,
        chat: `<svg viewBox="0 0 24 24"><path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M20,16H5.17L4,17.17V4H20V16Z"/></svg>`,
        close: `<svg viewBox="0 0 24 24"><path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/></svg>`,
        send: `<svg viewBox="0 0 24 24"><path d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/></svg>`,
        chevron: `<svg viewBox="0 0 24 24"><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/></svg>`,
        shield: `<svg viewBox="0 0 24 24"><path d="M12,22C17.07,18.76 20,14.07 20,10V4L12,1L4,4V10C4,14.07 6.93,18.76 12,22Z"/></svg>`,
        support: `<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12C2 13.66 2.42 15.21 3.17 16.57L2 22L7.66 20.87C8.97 21.59 10.45 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2M13 17H11V15H13V17M13 13H11V7H13V13Z"/></svg>`
    };

    function initWidget() {
        // 4. Create DOM elements
        const widgetContainer = document.createElement('div');
        widgetContainer.className = 'docagent-widget-container';

        // Panel
        const panel = document.createElement('div');
        panel.className = 'docagent-widget-panel closed';
        panel.innerHTML = `
            <div class="docagent-widget-header">
                <div class="docagent-widget-header-info">
                    <div class="docagent-widget-header-avatar">
                        ${SVGS.robot}
                    </div>
                    <div class="docagent-widget-header-details">
                        <span class="docagent-widget-header-name">${escapeHtml(botName)}</span>
                        <span class="docagent-widget-header-status">
                            <span class="docagent-widget-header-dot"></span>
                            Active Assistant
                        </span>
                    </div>
                </div>
                <button class="docagent-widget-header-close" title="Close chat">
                    ${SVGS.close}
                </button>
            </div>
            <div class="docagent-widget-chat-history"></div>
            <div class="docagent-widget-inquiry-view" style="display: none;">
                <div class="docagent-widget-inquiry-header">
                    <div class="docagent-widget-inquiry-badge">
                        ${SVGS.support} Direct HR Inquiry
                    </div>
                    <h3 class="docagent-widget-inquiry-title">Contact HR / Admin Support</h3>
                    <p class="docagent-widget-inquiry-desc">Have a specific question, policy exception, or request? Submit directly to the Admin Dashboard for review.</p>
                </div>
                <div class="docagent-widget-form-card">
                    <div class="docagent-widget-form-group">
                        <label class="docagent-widget-form-label">
                            <span>Your Email Address</span>
                            <span style="color: #EF4444;">*</span>
                        </label>
                        <input type="email" class="docagent-widget-form-input docagent-inquiry-email" placeholder="e.g. employee@company.com" autocomplete="email" />
                    </div>
                    <div class="docagent-widget-form-group">
                        <label class="docagent-widget-form-label">
                            <span>Inquiry Title / Subject</span>
                            <span style="color: #EF4444;">*</span>
                        </label>
                        <input type="text" class="docagent-widget-form-input docagent-inquiry-title" placeholder="e.g. Leave request exception or clarification" />
                    </div>
                    <div class="docagent-widget-form-group">
                        <label class="docagent-widget-form-label">
                            <span>Description / Details</span>
                            <span style="color: #EF4444;">*</span>
                        </label>
                        <textarea class="docagent-widget-form-textarea docagent-inquiry-desc" rows="4" placeholder="Provide full details for the HR admin team..."></textarea>
                    </div>
                    <div class="docagent-widget-form-error"></div>
                    <div class="docagent-widget-form-actions">
                        <button type="button" class="docagent-widget-form-cancel">Back to Chat</button>
                        <button type="button" class="docagent-widget-form-submit">
                            <span>Send to Admin</span>
                            ${SVGS.send}
                        </button>
                    </div>
                </div>
            </div>
            <div class="docagent-widget-footer">
                <div class="docagent-widget-pill-bar">
                    <button type="button" class="docagent-widget-pill-btn" title="Contact HR / Admin with a specific question or request">
                        ${SVGS.support}
                        <span>Contact HR / Admin</span>
                    </button>
                </div>
                <div class="docagent-widget-input-row">
                    <textarea class="docagent-widget-input" placeholder="Ask a question about policies..." rows="1" style="border: none !important; outline: none !important; box-shadow: none !important; -webkit-box-shadow: none !important; background: transparent !important;"></textarea>
                    <button class="docagent-widget-send-btn" disabled title="Send message">
                        ${SVGS.send}
                    </button>
                </div>
                <a href="${apiUrl}" target="_blank" class="docagent-widget-brand-link">
                    Powered by ${SVGS.shield} DocAgent AI
                </a>
            </div>
        `;

        // Launcher
        const launcher = document.createElement('button');
        launcher.className = 'docagent-widget-launcher';
        launcher.setAttribute('aria-label', 'Open chatbot');

        function renderLauncherIcon() {
            if (launcherImage) {
                launcher.innerHTML = `<img src="${escapeHtml(launcherImage)}" alt="" />`;
                launcher.querySelector('img').addEventListener('error', () => {
                    launcherImage = '';
                    renderLauncherIcon();
                });
            } else {
                launcher.innerHTML = state.isOpen ? SVGS.close : SVGS.chat;
            }
        }
        renderLauncherIcon();

        widgetContainer.appendChild(panel);
        widgetContainer.appendChild(launcher);
        document.body.appendChild(widgetContainer);

        // Dom elements references
        const chatHistoryEl = panel.querySelector('.docagent-widget-chat-history');
        const footerEl = panel.querySelector('.docagent-widget-footer');
        const inputEl = panel.querySelector('.docagent-widget-input');
        const sendBtnEl = panel.querySelector('.docagent-widget-send-btn');
        const closeBtnEl = panel.querySelector('.docagent-widget-header-close');
        const pillBtnEl = panel.querySelector('.docagent-widget-pill-btn');
        const inquiryViewEl = panel.querySelector('.docagent-widget-inquiry-view');
        const inquiryEmailEl = panel.querySelector('.docagent-inquiry-email');
        const inquiryTitleEl = panel.querySelector('.docagent-inquiry-title');
        const inquiryDescEl = panel.querySelector('.docagent-inquiry-desc');
        const inquiryErrorEl = panel.querySelector('.docagent-widget-form-error');
        const inquiryCancelBtn = panel.querySelector('.docagent-widget-form-cancel');
        const inquirySubmitBtn = panel.querySelector('.docagent-widget-form-submit');

        // 5. Message rendering functions
        function appendMessage(sender, text, context = null) {
            const msgWrapper = document.createElement('div');
            msgWrapper.className = `docagent-widget-msg docagent-widget-msg-${sender}`;

            const avatar = document.createElement('div');
            avatar.className = 'docagent-widget-msg-avatar';
            avatar.innerHTML = sender === 'user' ? SVGS.user : SVGS.robot;

            const bubble = document.createElement('div');
            bubble.className = 'docagent-widget-msg-bubble';

            if (sender === 'user') {
                bubble.textContent = text;
            } else {
                bubble.innerHTML = formatMarkdown(text);

                // Sources / Referenced documents
                if (context && context.length > 0) {
                    const sourcesContainer = document.createElement('div');
                    sourcesContainer.className = 'docagent-widget-sources';

                    const toggleBtn = document.createElement('button');
                    toggleBtn.className = 'docagent-widget-sources-btn';
                    toggleBtn.innerHTML = `${SVGS.chevron} View ${context.length} referenced source(s)`;

                    const contentList = document.createElement('div');
                    contentList.className = 'docagent-widget-sources-content';

                    context.forEach((chunk, index) => {
                        const item = document.createElement('div');
                        item.className = 'docagent-widget-source-item';
                        const score = chunk.score ? (chunk.score * 100).toFixed(0) : '95';
                        item.innerHTML = `
                            <div class="docagent-widget-source-header">
                                <span class="docagent-widget-source-title">[${index + 1}] ${escapeHtml(chunk.filename)}</span>
                                <span class="docagent-widget-source-badge">Match: ${score}%</span>
                            </div>
                            <p class="docagent-widget-source-text">"${escapeHtml(chunk.text.substring(0, 140))}..."</p>
                        `;
                        contentList.appendChild(item);
                    });

                    toggleBtn.addEventListener('click', () => {
                        const isHidden = contentList.style.display === 'none' || contentList.style.display === '';
                        contentList.style.display = isHidden ? 'flex' : 'none';
                        toggleBtn.classList.toggle('active', isHidden);
                    });

                    sourcesContainer.appendChild(toggleBtn);
                    sourcesContainer.appendChild(contentList);
                    bubble.appendChild(sourcesContainer);
                }
            }

            msgWrapper.appendChild(avatar);
            msgWrapper.appendChild(bubble);
            chatHistoryEl.appendChild(msgWrapper);
            chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
        }

        function appendTypingIndicator() {
            const indicatorId = 'docagent-typing-' + Date.now();
            const msgWrapper = document.createElement('div');
            msgWrapper.className = 'docagent-widget-msg docagent-widget-msg-agent';
            msgWrapper.id = indicatorId;

            const avatar = document.createElement('div');
            avatar.className = 'docagent-widget-msg-avatar';
            avatar.innerHTML = SVGS.robot;

            const bubble = document.createElement('div');
            bubble.className = 'docagent-widget-msg-bubble';
            bubble.innerHTML = `
                <div class="docagent-widget-typing">
                    <span class="docagent-widget-typing-dot"></span>
                    <span class="docagent-widget-typing-dot"></span>
                    <span class="docagent-widget-typing-dot"></span>
                </div>
            `;

            msgWrapper.appendChild(avatar);
            msgWrapper.appendChild(bubble);
            chatHistoryEl.appendChild(msgWrapper);
            chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
            return indicatorId;
        }

        function removeTypingIndicator(indicatorId) {
            const el = document.getElementById(indicatorId);
            if (el) el.remove();
        }

        // 6. Action handlers
        let closeTimeout = null;
        function toggleChat(forceOpen = null) {
            state.isOpen = forceOpen !== null ? forceOpen : !state.isOpen;
            if (closeTimeout) {
                clearTimeout(closeTimeout);
                closeTimeout = null;
            }
            if (state.isOpen) {
                panel.classList.remove('closed');
                // Force browser reflow to guarantee CSS transition plays cleanly from hidden state
                void panel.offsetHeight;
                panel.classList.add('open');
                launcher.classList.add('open');
                renderLauncherIcon();
                inputEl.focus();

                // Greet on first open
                if (!state.hasGreeted) {
                    appendMessage('agent', greetingMsg);
                    state.hasGreeted = true;
                }
            } else {
                panel.classList.remove('open');
                launcher.classList.remove('open');
                renderLauncherIcon();
                closeTimeout = setTimeout(() => {
                    if (!state.isOpen) {
                        panel.classList.add('closed');
                    }
                }, 260);
            }
        }

        async function handleSendMessage() {
            const text = inputEl.value.trim();
            if (!text || state.isTyping) return;

            // Clear input
            inputEl.value = '';
            inputEl.style.height = 'auto';
            sendBtnEl.disabled = true;

            // Render user message
            appendMessage('user', text);
            state.chatHistory.push({ role: 'user', text: text });

            // Show typing indicator
            state.isTyping = true;
            const typingId = appendTypingIndicator();

            try {
                const response = await fetch(`${apiUrl}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        query: text,
                        chat_history: state.chatHistory.slice(-10),
                        chatbot_id: chatbotId
                    })
                });

                removeTypingIndicator(typingId);
                state.isTyping = false;

                if (response.ok) {
                    const data = await response.json();
                    appendMessage('agent', data.answer, data.context);
                    state.chatHistory.push({ role: 'model', text: data.answer });
                } else {
                    appendMessage('agent', '⚠️ Sorry, there was an issue processing your query. Please try again.');
                }
            } catch (error) {
                removeTypingIndicator(typingId);
                state.isTyping = false;
                console.error('Chat error:', error);
                appendMessage('agent', '⚠️ Connection error. Could not reach the chatbot service.');
            }
        }

        // 6b. Inquiry handlers
        function openInquiryView() {
            chatHistoryEl.style.display = 'none';
            footerEl.style.display = 'none';
            inquiryViewEl.style.display = 'flex';
            inquiryErrorEl.style.display = 'none';
            inquiryEmailEl.focus();
        }

        function closeInquiryView() {
            inquiryViewEl.style.display = 'none';
            chatHistoryEl.style.display = 'flex';
            footerEl.style.display = 'flex';
            chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
            inputEl.focus();
        }

        function showInquiryError(msg) {
            inquiryErrorEl.textContent = msg;
            inquiryErrorEl.style.display = 'block';
        }

        async function handleSendInquiry() {
            const email = inquiryEmailEl.value.trim();
            const title = inquiryTitleEl.value.trim();
            const desc = inquiryDescEl.value.trim();

            if (!email) {
                showInquiryError("Please enter your work or personal email address.");
                inquiryEmailEl.focus();
                return;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showInquiryError("Please enter a valid email address (e.g. name@company.com).");
                inquiryEmailEl.focus();
                return;
            }

            if (!title) {
                showInquiryError("Please enter an inquiry title / subject.");
                inquiryTitleEl.focus();
                return;
            }

            if (!desc) {
                showInquiryError("Please describe your request or question in the description field.");
                inquiryDescEl.focus();
                return;
            }

            inquiryErrorEl.style.display = 'none';
            inquirySubmitBtn.disabled = true;
            inquirySubmitBtn.innerHTML = `<span>Sending...</span>`;

            try {
                const response = await fetch(`${apiUrl}/api/widget/inquiry`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        chatbot_id: chatbotId,
                        email: email,
                        title: title,
                        description: desc
                    })
                });

                if (response.ok) {
                    // Reset fields
                    inquiryEmailEl.value = '';
                    inquiryTitleEl.value = '';
                    inquiryDescEl.value = '';

                    // Return to chat interface
                    closeInquiryView();

                    // Append confirmation to chat so user can seamlessly continue
                    appendMessage('agent', `### 📨 Inquiry Submitted to HR Admin\n\n**Subject:** ${escapeHtml(title)}\n**Contact Email:** \`${escapeHtml(email)}\`\n\nYour inquiry has been successfully forwarded to the Admin Dashboard for review. Our HR administration team will inspect your request and reach out.\n\nYou can continue asking policy questions below! ✨`);
                    chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
                    inputEl.focus();
                } else {
                    const err = await response.json().catch(() => ({}));
                    showInquiryError(err.detail || "Failed to submit inquiry. Please try again.");
                }
            } catch (err) {
                console.error("Inquiry error:", err);
                showInquiryError("Connection error. Could not reach the server.");
            } finally {
                inquirySubmitBtn.disabled = false;
                inquirySubmitBtn.innerHTML = `<span>Send to Admin</span> ${SVGS.send}`;
            }
        }

        // 7. Event listeners
        launcher.addEventListener('click', () => toggleChat());
        closeBtnEl.addEventListener('click', () => toggleChat(false));

        pillBtnEl.addEventListener('click', openInquiryView);
        inquiryCancelBtn.addEventListener('click', closeInquiryView);
        inquirySubmitBtn.addEventListener('click', handleSendInquiry);

        inputEl.addEventListener('input', () => {
            inputEl.style.height = 'auto';
            inputEl.style.height = Math.min(inputEl.scrollHeight, 90) + 'px';
            sendBtnEl.disabled = inputEl.value.trim() === '';
        });

        inputEl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        });

        sendBtnEl.addEventListener('click', handleSendMessage);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }
})();
