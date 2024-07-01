import axios from 'axios';
import Cookies from 'js-cookie';

import appStore from '../store/app';

const instance = axios.create({
  cache: 'no-cache',
  mode: 'same-origin',
  credentials: 'same-origin',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken'),
  },
});

instance.interceptors.request.use(
  function (config) {
    appStore.isLoading = true;
    return config;
  },
  function (error) {
    appStore.isLoading = false;
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    appStore.isLoading = false;
    return response;
  },
  (error) => {
    appStore.isLoading = false;
    return Promise.reject(error);
  }
);

export default instance;

// Projects
export function projectListUrl() {
  return `/api/projects/?limit=1000`;
}

export function projectUrl(projectId) {
  return `/api/projects/${projectId}/`;
}

export function userProjectStatusListUrl() {
  return `/api/userprojectstatus/`;
}

export function userProjectStatusUrl(userProjectStatusId) {
  return `/api/userprojectstatus/${userProjectStatusId}/`;
}

// Organization
export function searchOrganizationsUrl(search) {
  return `/api/organizations/?search=${search}`;
}

// Topic
export function searchTopicsUrl(search, restrict_to) {
  return `/api/topics/?search=${search}&restrict_to=${restrict_to}`;
}

// Tasks
export function taskUrl(projectId, taskId) {
  return `/api/projects/${projectId}/tasks/${taskId}/`;
}

export function tasksUrl(projectId) {
  return `/api/projects/${projectId}/tasks/`;
}

export function moveTaskUrl(projectId, taskId) {
  return `/api/projects/${projectId}/tasks/${taskId}/move/`;
}

export function taskNotificationsUrl(projectId, taskId) {
  return `/api/projects/${projectId}/tasks/${taskId}/notifications/`;
}

export function markTaskNotificationsAsReadUrl(projectId, taskId) {
  return `/api/projects/${projectId}/tasks/${taskId}/notifications/mark_all_as_read/`;
}

export function notificationsMarkAsReadByIdUrl(notificationId) {
  return `/api/notifications/mark-one-as-read/${notificationId}/`;
}

export function markAllNotificationsAsReadUrl() {
  return '/api/notifications/mark-all-as-read';
}

export function followupsUrl(projectId, taskId) {
  return `/api/projects/${projectId}/tasks/${taskId}/followups/`;
}

export function followupUrl(projectId, taskId, followupId) {
  return `/api/projects/${projectId}/tasks/${taskId}/followups/${followupId}/`;
}

export function resourcePreviewUrl(resourceId) {
  return `/ressource/${resourceId}/embed`;
}

// Regions
export function regionListUrl() {
  return `/api/regions/?limit=1000`;
}

// Communes
export function communeListUrl(postal) {
  return `/api/communes/?postal=${postal}&limit=1000`;
}

// Resources
export function resourceListUrl() {
  return `/api/resources/?limit=1000`;
}

// Challenges
export function challengeUrl(code) {
  return `/api/challenges/${code}/`;
}

// Challenges Definitions
export function challengeDefinitionUrl(code) {
  return `/api/challenges/definitions/${code}`;
}

// Non API routes
// TODO : Make them into proper endpoints
export function editTaskUrl(taskId, next = null) {
  return next
    ? `/task/${taskId}/update/?next=${next}`
    : `/task/${taskId}/update/`;
}

export function deleteTaskUrl(taskId) {
  return `/task/${taskId}/delete/`;
}

export function deleteTaskReminderUrl(taskId) {
  return `/task/${taskId}/remind-delete/`;
}

export function editReminderUrl(taskId) {
  return `/task/${taskId}/remind/`;
}
