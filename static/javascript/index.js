function onload_index() {

};

function map_showlocation(name, address, town) {
  iFrame_map = document.getElementById("LocationMap")
  iFrame_map.src="https://www.google.com/maps/embed/v1/place?key=AIzaSyAGMjgKmdqusYOmN1qv2GpE5_mU2RS9Mzo&q=" + name + "," + address + "," + town
};
