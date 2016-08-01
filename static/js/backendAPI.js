export class BackendAPI {
  constructor(config) {
    this.base_url = config.base_url;
    this.school_locations_endpoint = config.school_locations_endpoint;
    this.school_info_endpoint = config.school_info_endpoint;
  }

  // promise to return all school locations from backend
  getAllSchoolLocations() {
    return $.getJSON(this.base_url + school_locations_endpoint);
  }

  handleSearch(query) {
    return $.post(BASE_URL, {"query": query});
  };
}