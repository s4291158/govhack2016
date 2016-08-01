export class Storage {
  constructor() {
    this.watchlist = [];
  }

  addToWatchlist(school) {
    this.watchlist.push(school);
  }

  removeFromWatchlist(school) {
    let i = watchlist.indexOf(school);
    if(i == -1)
      throw new Error('school not found on watchlist');
    
    watchlist.splice(i, 1);
  }

  clearWatchlist() {
    watchlist = [];
  }
}

// TODO: add cookies