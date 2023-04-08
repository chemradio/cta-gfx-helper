import { redirect } from "@sveltejs/kit";

export const load = ({ locals }) => {
  throw redirect(302, "/orders");
  // return { data: locals };
};
