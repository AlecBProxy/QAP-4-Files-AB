let Customer = {
  firstName: "Hakeem Olajuwon",
  birthDate: "1963-01-21",
  gender: "Male",
  roomPreferences: ["King Bed", "Rockets Jerseys", "Championship Trophy"],
  paymentMethod: "Cash",
  affiliation: "Houston Rockets",
  position: "Center",

  mailingAddress: {
    street: "24 Space Street",
    city: "Houston",
    state: "Texas",
    zipCode: "77001",
  },
  phoneNumber: "(713)-111-1111",

  checkInDate: {
    year: 2024,
    month: 7,
    day: 10,
  },

  checkOutDate: {
    year: 2024,
    month: 7,
    day: 20,
  },

  // Method for acquiring age
  getAge: function () {
    let today = new Date();
    let birthDate = new Date(this.birthDate);
    let age = today.getFullYear() - birthDate.getFullYear();
    let monthDiff = today.getUTCMonth() - birthDate.getMonth();
    if (
      monthDiff < 0 ||
      (monthDiff === 0 && today.getDate() < birthDate.getDate())
    ) {
      age--;
    }
    return age;
  },

  //Method for acquiring duration of stay
  getStayDuration: function () {
    let checkIn = new Date(
      this.checkInDate.year,
      this.checkInDate.month - 1,
      this.checkInDate.day
    );
    let checkOut = new Date(
      this.checkOutDate.year,
      this.checkOutDate.month - 1,
      this.checkOutDate.day
    );
    //Miliseconds to days
    let duration = (checkOut - checkIn) / (1000 * 60 * 60 * 24);
    return Math.round(duration);
  },

  getDescription: function () {
    return `
    <p>Customer Name ${this.firstName}</p>
    <p>Birth Date: ${this.birthDate} (Age: ${this.getAge()})</p>
    <p>Gender: ${this.gender}</p>
    <p>Room Preferences: ${this.roomPreferences.join(", ")}</p>
    <p>Payment Method: ${this.paymentMethod}</p>
    <p>Mailing Address: ${this.mailingAddress.street}, ${
      this.mailingAddress.city
    }, ${this.mailingAddress.state}, ${this.mailingAddress.zipCode}</p>
    <p>Phone #: ${this.phoneNumber}</p>
    <p>Check-In Date: ${this.checkInDate.year}, ${this.checkInDate.month}, ${
      this.checkInDate.day
    }</p>
    <p>Check-out Date: ${this.checkOutDate.year}, ${this.checkOutDate.month}, ${
      this.checkOutDate.day
    }</p>
    <p>Duration of Stay: ${this.getStayDuration()} days</p>
    <p>Affiliated Team: ${this.affiliation}</P>
    <p>Playing Position: ${this.position}</p> 
    `;
  },

  displayDescription: function () {
    document.getElementById("customer-info").innerHTML = this.getDescription();
  },
};

//Sample to Console
console.log(Customer.getDescription());

window.onload = function () {
  Customer.displayDescription();
};
