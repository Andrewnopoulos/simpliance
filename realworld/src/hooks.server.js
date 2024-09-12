/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	const jwt = event.cookies.get('jwt');
	// console.log(jwt)
    if (jwt) {
        // The JWT is now the raw access token, no need to decode
        event.locals.user = { token: jwt };

        // Optionally, you can decode the JWT payload here if needed
        // But be aware this doesn't verify the token's signature
        try {
            const [header, payload, signature] = jwt.split('.');
            const decodedPayload = JSON.parse(atob(payload));
            event.locals.user = { ...event.locals.user, ...decodedPayload };
			// console.log(event.locals.user)
        } catch (error) {
            console.error('Error decoding JWT:', error);
        }
    } else {
        event.locals.user = null;
    }

    // Resolve the request
    const response = await resolve(event);

    // Add CORS headers
    response.headers.set('Access-Control-Allow-Origin', process.env.ORIGIN);
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    response.headers.set('Access-Control-Allow-Credentials', 'true');

    return response;
}