export const updateAuthUI = (isAuthenticated, username = '') => {
  const elements = getElements();
  elements.authSection.style.display = isAuthenticated ? 'none' : 'block';
  elements.appSection.style.display = isAuthenticated ? 'block' : 'none';
  if (isAuthenticated && username) {
    elements.usernameDisplay.textContent = username;
  }
};

export const showNotification = (message, type = 'info') => {
  // In production: Use a proper notification system
  console[type](message);
  alert(`${type.toUpperCase()}: ${message}`);
};

export const setDefaultDatetimes = () => {
  const elements = getElements();
  const now = new Date();
  const yesterday = new Date(now);
  yesterday.setDate(now.getDate() - 1);
  
  elements.sleepForm.start.value = yesterday.toISOString().slice(0, 16);
  elements.sleepForm.end.value = now.toISOString().slice(0, 16);
};

