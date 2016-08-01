export class UserInterface {
  constructor(ids, cbs) {
    // the $ preceding these objects show that they are jquery objects
    this.$searchBarInput = $('#' + ids.searchBar);
    this.$watchlistButton = $('#' + ids.watchlistButton);
    this.$compareSchoolsButton = $('#' + ids.compareSchoolsButton);
    this.initUI(
      cbs.searchBarInput, 
      cbs.watchListPress, 
      cbs.compareSchoolsPress);
  }

  initUI(onSearchCB, onWatchlistCB, onCompareCB) {
    // handle search input
    this.$searchBarInput.keypress(handleSearchKeyPress(onSearchCB));

    this.$watchlistButton.click(onWatchlistCB);

    this.$compareSchoolsButton.click(onCompareCB);
    
    // enable materialize side-menu
    $('.button-collapse').sideNav();
  }

  handleSearchKeyPress(cb) {
    return (e) => {
      const ENTER_KEY_CODE = 13;
      let key = e.which;
      if(key == ENTER_KEY_CODE){
        // this is probably going to the backend API
        cb(this.$searchBarInput.val());
      }
    }
  }
}