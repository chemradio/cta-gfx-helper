const isDocker = import.meta.env.VITE_IS_DOCKER === "true";

export const dispatcherURL = isDocker
    ? "http://dispatcher:9000"
    : "http://127.0.0.1:9000";
export const dispatcherLoginURL = `${dispatcherURL}/web_api/users/sessions/`;
export const dispatcherVerifyToken = `${dispatcherURL}/web_api/users/verify_token/`;
export const dispatcherRegisterURL = `${dispatcherURL}/web_api/users/`;
export const dispatcherOrdersURL = `${dispatcherURL}/web_api/orders/`;
