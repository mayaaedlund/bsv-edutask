describe('Tasks', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let firstname // firsname of user
    let lastname // last name of user
    let email // email of the user
  
    //before
    before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid
            firstname = user.firstName
            lastname = user.lastName
            email = user.email
          })
        })
    })
  
    beforeEach(function () {
      cy.visit('http://localhost:3000');
  
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email);
  
      cy.get('form').submit();
    });
  
    it('land on mainpage', function () {
      cy.get('h1')
      .should('contain.text', `Your tasks, ${firstname} ${lastname}`);
    });
  
    after(function () {
      // clean up by deleting the user from the database
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
  });
  