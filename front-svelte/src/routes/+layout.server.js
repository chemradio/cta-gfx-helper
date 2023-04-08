export const load = ({ locals }) => {
  if (locals.user) {
    console.log("user is OK");
    console.log("user is:", locals.user);
    return { user: locals.user };
  } else {
    console.log("user is empty");
    return { user: null };
  }
};
