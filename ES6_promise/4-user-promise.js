// 4-user-promise.js

export default function signUpUser(firstName, lastName) {
  return new Promise((resolve) => {
    resolve({
      firstName,
      lastName,
    });
  });
}
