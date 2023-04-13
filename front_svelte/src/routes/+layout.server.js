export const load = ({ locals }) => {
    if (Object.keys(locals.user).length > 0) {
        return { user: locals.user, toasts: locals.toasts };
    } else {
        return { user: null, toasts: locals.toasts };
    }
};
