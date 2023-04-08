import { dispatcherLoginURL } from "../config";

let sessions = [];

export const handleUserSubmit = async (email, password) => {
  const formData = new FormData();
  formData.append("email", email);
  formData.append("password", password);

  const res = fetch(dispatcherLoginURL, {
    method: "POST",
    body: formData,
    credentials: "include", // include cookies in the request
    headers: {
      Cookie: document.cookie,
    },
  })
    .then((response) => {
      console.log("response status is: ", response.status);
      if (response.status === 200) {
        return response.json();
      } else {
        // handle error response
        console.log("Invalid credentials. Try again.");
        return null;
        // return { status: 403, message: "Unauthorized. Invalid credentials." };
      }
    })
    .catch((error) => {
      // handle network or fetch error
      console.log(error);
      return null;
      // return { status: 500, message: "Server error." };
    });

  return await res;
};
