export const getElements = () => ({
  authSection: document.getElementById('auth'),
  appSection: document.getElementById('app'),
  usernameDisplay: document.getElementById('who'),
  registerForm: {
    username: document.getElementById('reg_user'),
    password: document.getElementById('reg_pass'),
    button: document.getElementById('btn_reg')
  },
  loginForm: {
    username: document.getElementById('login_user'),
    password: document.getElementById('login_pass'),
    button: document.getElementById('btn_login')
  },
  sleepForm: {
    start: document.getElementById('start'),
    end: document.getElementById('end'),
    notes: document.getElementById('notes'),
    button: document.getElementById('btn_add')
  },
  statsDisplay: document.getElementById('stats'),
  csvExport: document.getElementById('csv')
});

export const getChartContext = () => {
  const canvas = document.getElementById('chart');
  return canvas ? canvas.getContext('2d') : null;
};

export const displayStats = (stats) => {
  const elements = getElements();
  if (elements.statsDisplay) {
    elements.statsDisplay.textContent = JSON.stringify(stats, null, 2);
  }
};

