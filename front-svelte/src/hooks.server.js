/** @type {import('@sveltejs/kit').Handle} */
import { redirect } from "@sveltejs/kit";
import { decodeJwtToken } from "./tools/jwt";

// export async function handle({ event, resolve }) {
//   const currentPathname = event.url.pathname;
//   const jwt = event.cookies.get("jwt");
//   if (currentPathname === "/newOrder") {
//     if (!jwt) {
//       console.log("jwt is empty or missing. throwing redirect");
//       throw redirect(302, "/login");
//     }
//
//   }
//   userStore.update((current) => JSON.stringify(jwt));
//   console.log("jwt: ", jwt);
//   return resolve(event);
// }

export async function handle({ event, resolve }) {
  console.log("enterend HANDLE hook");
  const currentPathname = event.url.pathname;
  const jwt = event.cookies.get("jwt");

  if (currentPathname === "/login") return resolve(event);

  if (!jwt) {
    console.log("JWT cookie is missing. Redirecting to LOGIN page.");
    throw redirect(302, "/login");
  }

  const user_data = decodeJwtToken(jwt);
  console.log("writing user to event.locals from hooks. user is: ", user_data);
  event.locals.user = user_data;

  return resolve(event);
}
