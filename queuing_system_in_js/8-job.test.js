const kue = require('kue');
const { expect } = require('chai');

const createPushNotificationsJobs = require('./8-job');

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('creates push notification jobs', () => {
    const jobs = [
      { phoneNumber: '1234567890', message: 'Hello!' },
      { phoneNumber: '9876543210', message: 'Hi there!' }
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql({ phoneNumber: '1234567890', message: 'Hello!' });
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql({ phoneNumber: '9876543210', message: 'Hi there!' });
  });
});
