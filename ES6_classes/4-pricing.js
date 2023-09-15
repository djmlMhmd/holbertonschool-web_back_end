export default class Pricing {
  constructor(amount, currency) {
    this._amount = amount;
    this._currency = currency;
  }

  // getter attributes
  get amount() {
    return this._amount;
  }

  get currency() {
    return this._currency;
  }

  // setter attributes
  set amount(newAmount) {
    this._amount = newAmount;
  }

  set currency(newCurrency) {
    this._currency = newCurrency;
  }

  displayFullPrice() {
    return `${this._amount} ${this._currency.name} (${this._currency.code})`;
  }

  static convertPrice(amount, conversionRate) {
    return amount * conversionRate;
  }
}
