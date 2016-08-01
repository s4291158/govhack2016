export class Utils {

  // converts name data into a more readable format
  static proNounify(text) {
    return text.split('_').join(' ')
        .replace(/( ([a-z]))|(^[a-z])/g, (l) => {
          return l.toUpperCase();
        });
  }
}