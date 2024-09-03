import { error } from '@sveltejs/kit';

const base = process.env.API_URL || 'http://localhost:8000/api';

// const base = process.env.API_URL || 'http://app-host:8000';

async function sendRaw({ method, path, token }) {

	const opts = { method, headers: {} };

	if (token) {
		opts.headers['Authorization'] = `Bearer ${token}`;
	}

	const res = await fetch(`${base}/${path}`, opts);
	if (res.ok || res.status === 422) {
		const text = await res.text();
		return text
	}

	error(res.status);
}

async function send({ method, path, data, token, type }) {
	const opts = { method, headers: {} };

	if (type == 'application/x-www-form-urlencoded') {
		opts.headers['Content-Type'] = type;
		opts.headers['accept'] = 'application/json';
		opts.body = data;
	} else if (data) {
		opts.headers['Content-Type'] = 'application/json';
		opts.body = JSON.stringify(data);
	}

	if (token) {
		opts.headers['Authorization'] = `Bearer ${token}`;
	}

	const res = await fetch(`${base}/${path}`, opts);
	if (res.ok || res.status === 422) {
		const text = await res.text();
		return text ? JSON.parse(text) : {};
	}

	error(res.status);
}

export function get(path, token) {
	return send({ method: 'GET', path, token });
}

export function del(path, token) {
	return send({ method: 'DELETE', path, token });
}

export function post(path, data, token) {
	return send({ method: 'POST', path, data, token });
}

export function put(path, data, token) {
	return send({ method: 'PUT', path, data, token });
}

export function postForm(path, data, token) {
	return send({ method: 'POST', path, data, token, type: 'application/x-www-form-urlencoded' });
}

export function getHTML(path, token) {
	return sendRaw({ method: 'GET', path, token });
}