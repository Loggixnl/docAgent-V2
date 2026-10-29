// // Central API client service with authorization token management

// let sessionToken = localStorage.getItem('docagent_session_token') || '';
// let onUnauthorizedCallback = null;

// export function setSessionToken(token) {
//   sessionToken = token || '';
//   if (token) {
//     localStorage.setItem('docagent_session_token', token);
//   } else {
//     localStorage.removeItem('docagent_session_token');
//   }
// }

// export function getSessionToken() {
//   return sessionToken;
// }

// export function setOnUnauthorized(callback) {
//   onUnauthorizedCallback = callback;
// }

// export async function authFetch(url, options = {}) {
//   options.headers = options.headers || {};
//   if (sessionToken) {
//     options.headers['Authorization'] = `Bearer ${sessionToken}`;
//   }

//   try {
//     const response = await fetch(url, options);
//     if (response.status === 401) {
//       if (onUnauthorizedCallback) {
//         onUnauthorizedCallback();
//       }
//       throw new Error("Session expired. Please log in again.");
//     }
//     return response;
//   } catch (e) {
//     throw e;
//   }
// }

// // Authentication API
// export async function loginUser(email, password) {
//   const res = await fetch('/api/auth/login', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ email, password })
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Authentication failed.");
//   }
//   return res.json();
// }

// export async function registerUser(email, password, confirmPassword) {
//   const res = await fetch('/api/auth/register', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({
//       email,
//       password,
//       confirm_password: confirmPassword
//     })
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Registration failed.");
//   }
//   return res.json();
// }

// export async function getMe() {
//   const res = await authFetch('/api/auth/me');
//   if (!res.ok) {
//     throw new Error("Failed to get current user.");
//   }
//   return res.json();
// }

// export async function logoutUser() {
//   if (sessionToken) {
//     try {
//       await fetch('/api/auth/logout', {
//         method: 'POST',
//         headers: { 'Authorization': `Bearer ${sessionToken}` }
//       });
//     } catch (e) {
//       console.error("Logout request failed:", e);
//     }
//   }
//   setSessionToken('');
// }

// // Documents & Stats API
// export async function getStats() {
//   const res = await authFetch('/api/stats');
//   if (!res.ok) {
//     throw new Error("Failed to fetch statistics.");
//   }
//   return res.json();
// }

// export async function getDocuments() {
//   const res = await authFetch('/api/documents');
//   if (!res.ok) {
//     throw new Error("Failed to fetch documents.");
//   }
//   return res.json();
// }

// export function uploadDocument(file, apiKey, onProgress) {
//   return new Promise((resolve, reject) => {
//     const formData = new FormData();
//     formData.append("file", file);
//     if (apiKey) {
//       formData.append("api_key", apiKey);
//     }

//     const xhr = new XMLHttpRequest();
//     xhr.open("POST", "/api/upload", true);
//     if (sessionToken) {
//       xhr.setRequestHeader("Authorization", `Bearer ${sessionToken}`);
//     }

//     xhr.upload.onprogress = (e) => {
//       if (e.lengthComputable && onProgress) {
//         const percent = Math.round((e.loaded / e.total) * 100);
//         onProgress(percent >= 100 ? 99 : percent);
//       }
//     };

//     xhr.onload = () => {
//       if (xhr.status === 200) {
//         try {
//           resolve(JSON.parse(xhr.responseText));
//         } catch (e) {
//           resolve({ success: true });
//         }
//       } else if (xhr.status === 401) {
//         if (onUnauthorizedCallback) onUnauthorizedCallback();
//         reject(new Error("Your session has expired. Please log in again."));
//       } else {
//         let errorMsg = "Could not upload document.";
//         try {
//           const response = JSON.parse(xhr.responseText);
//           errorMsg = response.detail || errorMsg;
//         } catch (e) {}
//         reject(new Error(errorMsg));
//       }
//     };

//     xhr.onerror = () => {
//       reject(new Error("A network error occurred while uploading."));
//     };

//     xhr.send(formData);
//   });
// }

// export async function deleteDocument(docId) {
//   const res = await authFetch(`/api/documents/${docId}`, { method: 'DELETE' });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not delete document.");
//   }
//   return res.json();
// }

// export async function getDocumentAnalysis(docId) {
//   const res = await authFetch(`/api/documents/${docId}/analysis`);
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not fetch document analysis.");
//   }
//   return res.json();
// }

// // Settings API
// export async function getSettings() {
//   const res = await authFetch('/api/settings');
//   if (!res.ok) {
//     throw new Error("Failed to fetch settings.");
//   }
//   return res.json();
// }

// export async function saveSettings(payload) {
//   const body = typeof payload === 'string' ? { api_key: payload } : payload;
//   const res = await authFetch('/api/settings', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(body)
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not save settings.");
//   }
//   return res.json();
// }


// // Chat Session API
// export async function createChatSession() {
//   const res = await authFetch('/api/chat-sessions', { method: 'POST' });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not create chat session.");
//   }
//   return res.json();
// }

// export async function getChatSessions() {
//   const res = await authFetch('/api/chat-sessions');
//   if (!res.ok) {
//     throw new Error("Failed to fetch chat sessions.");
//   }
//   return res.json();
// }

// export async function getChatSession(sessionId) {
//   const res = await authFetch(`/api/chat-sessions/${sessionId}`);
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not fetch chat session.");
//   }
//   return res.json();
// }

// export async function deleteChatSession(sessionId) {
//   const res = await authFetch(`/api/chat-sessions/${sessionId}`, { method: 'DELETE' });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not delete chat session.");
//   }
//   return res.json();
// }

// // Chat API (supports stateless admin chats or stateful user sessions)
// export async function sendChatMessage({ query, chatHistory, model, provider, chatbotId, apiKey, sessionId, saveSession = false, baseUrl = null }) {
//   const headers = { 'Content-Type': 'application/json' };
//   if (apiKey) {
//     headers['X-API-Key'] = apiKey;
//   }
//   if (sessionToken) {
//     headers['Authorization'] = `Bearer ${sessionToken}`;
//   }

//   const res = await fetch('/api/chat', {
//     method: 'POST',
//     headers,
//     body: JSON.stringify({
//       query,
//       chat_history: chatHistory.slice(-10),
//       model,
//       provider,
//       chatbot_id: chatbotId,
//       session_id: sessionId || null,
//       save_session: saveSession,
//       base_url: baseUrl
//     })
//   });

//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "An error occurred while generating a response.");
//   }
//   return res.json();
// }


// // Admin Dashboard API
// export async function getAdminAnalytics() {
//   const res = await authFetch('/api/admin/analytics');
//   if (!res.ok) {
//     throw new Error("Failed to fetch analytics.");
//   }
//   return res.json();
// }

// export async function getAdminSessions(search = '', limit = 50, offset = 0) {
//   const params = new URLSearchParams({ search, limit, offset });
//   const res = await authFetch(`/api/admin/sessions?${params}`);
//   if (!res.ok) {
//     throw new Error("Failed to fetch admin sessions.");
//   }
//   return res.json();
// }

// export async function getAdminSessionDetail(sessionId) {
//   const res = await authFetch(`/api/admin/sessions/${sessionId}`);
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not fetch session detail.");
//   }
//   return res.json();
// }

// export async function getAdminQuestions(search = '', status = '', questionType = '', limit = 50, offset = 0) {
//   const params = new URLSearchParams({ search, status, question_type: questionType, limit, offset });
//   const res = await authFetch(`/api/admin/questions?${params}`);
//   if (!res.ok) {
//     throw new Error("Failed to fetch admin questions.");
//   }
//   return res.json();
// }

// export async function getAdminQuestionDetail(questionId) {
//   const res = await authFetch(`/api/admin/questions/${questionId}`);
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not fetch question detail.");
//   }
//   return res.json();
// }

// export async function updateAdminQuestion(questionId, data) {
//   const res = await authFetch(`/api/admin/questions/${questionId}`, {
//     method: 'PUT',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data)
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not update question.");
//   }
//   return res.json();
// }

// export async function submitWidgetInquiry(data) {
//   const res = await fetch('/api/widget/inquiry', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data)
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not submit inquiry.");
//   }
//   return res.json();
// }

// export async function deleteAdminSession(sessionId) {
//   const res = await authFetch(`/api/admin/sessions/${sessionId}`, {
//     method: 'DELETE'
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not delete chat session.");
//   }
//   return res.json();
// }

// export async function deleteAdminQuestion(questionId) {
//   const res = await authFetch(`/api/admin/questions/${questionId}`, {
//     method: 'DELETE'
//   });
//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Could not delete query.");
//   }
//   return res.json();
// }







// for railway 


// Central API client service with authorization token management

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '')
  .replace(/\/+$/, '');

function apiUrl(url) {
  if (/^https?:\/\//i.test(url)) return url;
  return `${API_BASE}${url.startsWith('/') ? url : `/${url}`}`;
}

let sessionToken = localStorage.getItem('docagent_session_token') || '';
let onUnauthorizedCallback = null;

export function setSessionToken(token) {
  sessionToken = token || '';
  if (token) {
    localStorage.setItem('docagent_session_token', token);
  } else {
    localStorage.removeItem('docagent_session_token');
  }
}

export function getSessionToken() {
  return sessionToken;
}

export function setOnUnauthorized(callback) {
  onUnauthorizedCallback = callback;
}

export async function authFetch(url, options = {}) {
  const headers = { ...(options.headers || {}) };

  if (sessionToken) {
    headers['Authorization'] = `Bearer ${sessionToken}`;
  }

  const response = await fetch(apiUrl(url), {
    ...options,
    headers
  });

  if (response.status === 401) {
    if (onUnauthorizedCallback) {
      onUnauthorizedCallback();
    }
    throw new Error('Session expired. Please log in again.');
  }

  return response;
}

// Authentication API
export async function loginUser(email, password) {
  const res = await fetch(apiUrl('/api/auth/login'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Authentication failed.');
  }

  return res.json();
}

export async function registerUser(email, password, confirmPassword) {
  const res = await fetch(apiUrl('/api/auth/register'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      password,
      confirm_password: confirmPassword
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Registration failed.');
  }

  return res.json();
}

export async function getMe() {
  const res = await authFetch('/api/auth/me');

  if (!res.ok) {
    throw new Error('Failed to get current user.');
  }

  return res.json();
}

export async function logoutUser() {
  if (sessionToken) {
    try {
      await fetch(apiUrl('/api/auth/logout'), {
        method: 'POST',
        headers: { Authorization: `Bearer ${sessionToken}` }
      });
    } catch (e) {
      console.error('Logout request failed:', e);
    }
  }

  setSessionToken('');
}

// Documents & Stats API
export async function getStats() {
  const res = await authFetch('/api/stats');

  if (!res.ok) {
    throw new Error('Failed to fetch statistics.');
  }

  return res.json();
}

export async function getDocuments() {
  const res = await authFetch('/api/documents');

  if (!res.ok) {
    throw new Error('Failed to fetch documents.');
  }

  return res.json();
}

export function uploadDocument(file, apiKey, onProgress) {
  return new Promise((resolve, reject) => {
    const formData = new FormData();
    formData.append('file', file);

    if (apiKey) {
      formData.append('api_key', apiKey);
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl('/api/upload'), true);

    if (sessionToken) {
      xhr.setRequestHeader('Authorization', `Bearer ${sessionToken}`);
    }

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && onProgress) {
        const percent = Math.round((e.loaded / e.total) * 100);
        onProgress(percent >= 100 ? 99 : percent);
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          resolve(JSON.parse(xhr.responseText));
        } catch (e) {
          resolve({ success: true });
        }
      } else if (xhr.status === 401) {
        if (onUnauthorizedCallback) onUnauthorizedCallback();
        reject(new Error('Your session has expired. Please log in again.'));
      } else {
        let errorMsg = 'Could not upload document.';

        try {
          const response = JSON.parse(xhr.responseText);
          errorMsg = response.detail || errorMsg;
        } catch (e) { }

        reject(new Error(errorMsg));
      }
    };

    xhr.onerror = () => {
      reject(new Error('A network error occurred while uploading.'));
    };

    xhr.send(formData);
  });
}

export async function deleteDocument(docId) {
  const res = await authFetch(`/api/documents/${docId}`, {
    method: 'DELETE'
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not delete document.');
  }

  return res.json();
}

export async function getDocumentAnalysis(docId) {
  const res = await authFetch(`/api/documents/${docId}/analysis`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not fetch document analysis.');
  }

  return res.json();
}

// Settings API
export async function getSettings() {
  const res = await authFetch('/api/settings');

  if (!res.ok) {
    throw new Error('Failed to fetch settings.');
  }

  return res.json();
}

export async function saveSettings(payload) {
  const body = typeof payload === 'string'
    ? { api_key: payload }
    : payload;

  const res = await authFetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not save settings.');
  }

  return res.json();
}

// Chat Session API
export async function createChatSession() {
  const res = await authFetch('/api/chat-sessions', {
    method: 'POST'
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not create chat session.');
  }

  return res.json();
}

export async function getChatSessions() {
  const res = await authFetch('/api/chat-sessions');

  if (!res.ok) {
    throw new Error('Failed to fetch chat sessions.');
  }

  return res.json();
}

export async function getChatSession(sessionId) {
  const res = await authFetch(`/api/chat-sessions/${sessionId}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not fetch chat session.');
  }

  return res.json();
}

export async function deleteChatSession(sessionId) {
  const res = await authFetch(`/api/chat-sessions/${sessionId}`, {
    method: 'DELETE'
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not delete chat session.');
  }

  return res.json();
}

// Chat API
export async function sendChatMessage({
  query,
  chatHistory,
  model,
  provider,
  chatbotId,
  apiKey,
  sessionId,
  saveSession = false,
  baseUrl = null
}) {
  const headers = { 'Content-Type': 'application/json' };

  if (apiKey) {
    headers['X-API-Key'] = apiKey;
  }

  if (sessionToken) {
    headers['Authorization'] = `Bearer ${sessionToken}`;
  }

  const res = await fetch(apiUrl('/api/chat'), {
    method: 'POST',
    headers,
    body: JSON.stringify({
      query,
      chat_history: chatHistory.slice(-10),
      model,
      provider,
      chatbot_id: chatbotId,
      session_id: sessionId || null,
      save_session: saveSession,
      base_url: baseUrl
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'An error occurred while generating a response.');
  }

  return res.json();
}

// Admin Dashboard API
export async function getAdminAnalytics() {
  const res = await authFetch('/api/admin/analytics');

  if (!res.ok) {
    throw new Error('Failed to fetch analytics.');
  }

  return res.json();
}

export async function getAdminSessions(search = '', limit = 50, offset = 0) {
  const params = new URLSearchParams({
    search,
    limit: String(limit),
    offset: String(offset)
  });

  const res = await authFetch(`/api/admin/sessions?${params}`);

  if (!res.ok) {
    throw new Error('Failed to fetch admin sessions.');
  }

  return res.json();
}

export async function getAdminSessionDetail(sessionId) {
  const res = await authFetch(`/api/admin/sessions/${sessionId}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not fetch session detail.');
  }

  return res.json();
}

export async function getAdminQuestions(
  search = '',
  status = '',
  questionType = '',
  limit = 50,
  offset = 0
) {
  const params = new URLSearchParams({
    search,
    status,
    question_type: questionType,
    limit: String(limit),
    offset: String(offset)
  });

  const res = await authFetch(`/api/admin/questions?${params}`);

  if (!res.ok) {
    throw new Error('Failed to fetch admin questions.');
  }

  return res.json();
}

export async function getAdminQuestionDetail(questionId) {
  const res = await authFetch(`/api/admin/questions/${questionId}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not fetch question detail.');
  }

  return res.json();
}

export async function updateAdminQuestion(questionId, data) {
  const res = await authFetch(`/api/admin/questions/${questionId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not update question.');
  }

  return res.json();
}

export async function submitWidgetInquiry(data) {
  const res = await fetch(apiUrl('/api/widget/inquiry'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not submit inquiry.');
  }

  return res.json();
}

export async function deleteAdminSession(sessionId) {
  const res = await authFetch(`/api/admin/sessions/${sessionId}`, {
    method: 'DELETE'
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not delete chat session.');
  }

  return res.json();
}

export async function deleteAdminQuestion(questionId) {
  const res = await authFetch(`/api/admin/questions/${questionId}`, {
    method: 'DELETE'
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not delete query.');
  }

  return res.json();
}