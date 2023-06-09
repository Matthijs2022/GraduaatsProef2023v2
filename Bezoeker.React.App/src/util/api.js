import axios from 'axios';

export function getBedrijven() {
  return axios
    .get('http://127.0.0.1:5000/bedrijven') //Dit is dus de nieuwe API in Python
    .then(function (response) {
      //console.log(response.data);
      return response.data;
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
    .finally(function () {
      // always executed
    });
}

// export function getBezoekersInBedrijf(BedrijfId) {
//   return axios
//     .get(
//       `https://localhost:7020/api/Bezoeker/GetBezoekersInBedrijf/${BedrijfId}`
//     )
//     .then(function (response) {
//       return response.data;
//     })
//     .catch(function (error) {
//       console.log(error);
//     })
//     .finally(function () {
//       //always executed
//     });
// }

// export function getParkeerPlaatsenVanBedrijf(BedrijfId) {
//   return axios
//     .get(`nog in te vullen`)
//     .then(function (response) {
//       return response.data;
//     })
//     .catch(function (error) {
//       console.log(error);
//     })
//     .finally(function () {
//       //always executed
//     });
// }
