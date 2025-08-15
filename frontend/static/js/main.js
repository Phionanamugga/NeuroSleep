import { AuthService } from './services/auth.service';
import { SleepService } from './services/sleep.service';
import { apiService } from './services/api.service';
import { getElements, setDefaultDatetimes } from './utils/dom.utils';


class SleepTrackerApp {
  constructor() {
    this.elements = getElements();
    this._initEventListeners();
    this._checkExistingSession();
    setDefaultDatetimes();
  }

  _initEventListeners() {
    this.elements.registerForm.button.addEventListener('click', this._handleRegister);
    this.elements.loginForm.button.addEventListener('click', this._handleLogin);
    this.elements.sleepForm.button.addEventListener('click', this._handleAddSleep);
    this.elements.csvExport.addEventListener('click', this._handleExportCSV);
  }

  _handleRegister = async () => {
    const { username, password } = this.elements.registerForm;
    await AuthService.register(username.value, password.value);
  };

  _handleLogin = async () => {
    const { username, password } = this.elements.loginForm;
    await AuthService.login(username.value, password.value);
  };

  _handleAddSleep = async () => {
    const { start, end, notes } = this.elements.sleepForm;
    await SleepService.addEntry({
      start: start.value,
      end: end.value,
      notes: notes.value
    });
    notes.value = '';
  };

  _handleExportCSV = (e) => {
    e.preventDefault();
    SleepService.exportCSV();
  };

  _checkExistingSession() {
    if (apiService.token) {
      updateAuthUI(true);
      SleepService.loadData();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new SleepTrackerApp();
});

document.getElementById('current-year').textContent = new Date().getFullYear();