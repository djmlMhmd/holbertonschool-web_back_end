const kue = require('kue');

const queue = kue.createQueue();
const job = queue.create('push_notification_code',
  {
    phoneNumber: '0606060606',
    message: 'Hello World',
  })
  .save((err) => {
    if (err) {
      console.log('Notification job failed');
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });
