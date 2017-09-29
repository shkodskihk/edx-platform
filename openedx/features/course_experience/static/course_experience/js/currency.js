import whichCountry from 'which-country';
import 'jquery.cookie';
import $ from 'jquery'; // eslint-disable-line import/extensions
import _ from 'underscore'; // eslint-disable-line import/extensions

export class Currency {  // eslint-disable-line import/prefer-default-export

  setCookie(countryCode, l10nData) {
    const userCountryData = _.pick(l10nData, countryCode);
    let countryL10nData = userCountryData[countryCode];

    if (countryL10nData) {
      countryL10nData.countryCode = countryCode;
    } else {
      countryL10nData = {
        countryCode: 'USA',
        symbol: '$',
        rate: '1',
        code: 'USD',
      };
    }
    this.countryL10nData = countryL10nData;
    $.cookie('edx-price-l10n', JSON.stringify(countryL10nData), {
      expires: 1,
    });
  }

  setPrice() {
    const l10nCookie = this.countryL10nData;
    const lmsregex = /(\$)(\d*)( USD)/g;
    const price = $('input[name="verified_mode"]').filter(':visible')[0];
    const regexMatch = lmsregex.exec(price.value);
    const dollars = parseFloat(regexMatch[2]);
    const converted = dollars * l10nCookie.rate;
    const string = `${l10nCookie.symbol}${Math.ceil(converted)} ${l10nCookie.code}`;
    // Use regex to change displayed price on track selection
    // based on edx-price-l10n cookie currency_data
    price.value = price.value.replace(regexMatch[0], string);
  }

  getL10nData(countryCode) {
    const l10nData = $('#currency_data').attr('value');
    if (l10nData) {
      this.setCookie(countryCode, l10nData);
    }
    this.setPrice();
  }

  getCountry(position) {
    const countryCode = whichCountry([position.coords.longitude, position.coords.latitude]);
    this.countryL10nData = JSON.parse($.cookie('edx-price-l10n'));

    if (countryCode) { // || flags.course_details_localize_price) {
      if (this.countryL10nData && this.countryL10nData.countryCode === countryCode) {
        // If pricing cookie has been set use it
        this.setPrice();
      } else {
        // Else make API call and set it
        this.getL10nData(countryCode);
      }
    } else {
      // If pricing cookie has been set use it
      this.setPrice();
    }
  }

  getUserLocation() {
    // Get user location from browser
    navigator.geolocation.getCurrentPosition(this.getCountry.bind(this));
  }

  constructor() {
    this.getUserLocation();
  }
}
