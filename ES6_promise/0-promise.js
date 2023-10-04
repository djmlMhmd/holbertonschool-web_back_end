function getResponseFromAPI() {
	return new Promise((resolve, reject) => {
		setTimeout(() => {
			const data = { message: 'API response data' };
			resolve(data);
		}, 2000);
	});
}

getResponseFromAPI
	.then((response) => {
		console.log('API Response', response);
	})
	.catch((error) => {
		console.error('Error', error);
	});
