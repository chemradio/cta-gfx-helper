import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  // remove current cookie if present
  event.cookies.delete("jwt");
  try {
    await event.fetch("http://127.0.0.1:8000/web_api/users/sessions", {
      method: "DELETE",
    });
  } catch (e) {
    console.log("Logout server reports error: ", e);
  }
  event.locals.user = {};
  throw redirect(307, "/login");
};
