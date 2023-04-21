

export function displayMessage(message, type='info') {
  this.$notify({ message: message, type: type});
  if (type === 'success') {
    console.log('%c' + message, 'color: green');
  } else if (type === 'error') {
    console.error(message);
  } else {
   console.log(message);
  };
};

