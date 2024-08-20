/** @type {import('@sveltejs/kit').Handle} */
export function handle({ event, resolve }) {
	const jwt = event.cookies.get('jwt');
	console.log(jwt)
    if (jwt) {
        // The JWT is now the raw access token, no need to decode
        event.locals.user = { token: jwt };

        // Optionally, you can decode the JWT payload here if needed
        // But be aware this doesn't verify the token's signature
        try {
            const [header, payload, signature] = jwt.split('.');
            const decodedPayload = JSON.parse(atob(payload));
            event.locals.user = { ...event.locals.user, ...decodedPayload };
			console.log(event.locals.user)
        } catch (error) {
            console.error('Error decoding JWT:', error);
        }
    } else {
        event.locals.user = null;
    }

	return resolve(event);
}
