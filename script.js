fetch('https://programsandcourses.anu.edu.au/data/CourseSearch/GetCourses?AppliedFilter=FilterByCourses&Source=&ShowAll=true&PageIndex=0&MaxPageSize=10&PageSize=Infinity&SortColumn=&SortDirection=&InitailSearchRequestedFromExternalPage=false&SearchText=&SelectedYear=2025&Careers%5B0%5D=&Careers%5B1%5D=&Careers%5B2%5D=&Careers%5B3%5D=&GraduateAttributes%5B0%5D=&GraduateAttributes%5B1%5D=&GraduateAttributes%5B2%5D=&OtherCriteria%5B0%5D=&OtherCriteria%5B1%5D=&Sessions%5B0%5D=&Sessions%5B1%5D=&Sessions%5B2%5D=&Sessions%5B3%5D=&Sessions%5B4%5D=&Sessions%5B5%5D=&DegreeIdentifiers%5B0%5D=&DegreeIdentifiers%5B1%5D=&DegreeIdentifiers%5B2%5D=&FilterByMajors=&FilterByMinors=&FilterBySpecialisations=&CollegeName=All+Colleges&ModeOfDelivery=All+Modes')
  .then(response => response.json())
  .then(data => {
    const jsonString = JSON.stringify(data.Items, null, 2);
    const fs = require('fs');
    fs.writeFileSync('courses.json', jsonString);
    
    console.log('Data has been written to courses.json');
    console.log(`Total courses saved: ${data.Items.length}`);
  })
  .catch(err => {
    console.error('Error fetching or saving data:', err);
  });