import { apiService } from './api.service';
import { updateAuthUI, showNotification } from '../utils/ui.utils';
import { sleepService } from './sleep.service';

export class AuthService {
  static async register(username, password) {
    try {
      const user = await apiService.register({ username, password });
      showNotification(`Welcome ${user.username}!`, 'success');
      return true;
    } catch (error) {
      showNotification(`Registration failed: ${error.message}`, 'error');
      return false;
    }
  }

  static async login(username, password) {
    try {
      const { access_token } = await apiService.login({ username, password });
      apiService.setToken(access_token);
      updateAuthUI(true, username);
      await sleepService.loadData();
      return true;
    } catch (error) {
      showNotification(`Login failed: ${error.message}`, 'error');
      return false;
    }
  }

  static logout() {
    apiService.setToken(null);
    updateAuthUI(false);
    showNotification('Logged out successfully', 'info');
  }
}

