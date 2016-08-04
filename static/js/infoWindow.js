export class InfoWindow {
  constructor(storage, config) {
    this.storage = storage;

    this.sel = config.infoDivSel;
  }

  openInfoWindow(school) {
    this.currentSchool = school;


  }

  handleSaveToWishlistButton_click(e) {
    this.storage.addToWatchlist(this.currentSchool);
  }
}