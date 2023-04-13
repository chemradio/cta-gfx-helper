import { dispatcherVerifyToken } from "../config";

export const authenticateUser = async (event) => {
  const jwt = event.cookies.get("jwt");

  try {
    const response = await event.fetch(dispatcherVerifyToken, {
      method: "GET",
      headers: {
        Authorization: jwt,
      },
    });

    if (response.ok) {
      const user = await response.json();
      return user;
    } else {
      return null;
    }
  } catch (err) {
    console.error("Error verifying token:", err);
    return null;
  }
};
