describe("Test CRUD of todo item", () => {
    let uid

    before(function () {
        // Add user
        cy.fixture("user.json").then((user) => {
            cy.request({
                method: "POST",
                url: "http://localhost:5000/users/create",
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid

                // Add task for user
                // This currently fails with status 500 Internal Server Error
                cy.fixture("task.json").then((task) => {
                    task.userid = uid
                    cy.request({
                        method: "POST",
                        url: "http://localhost:5000/tasks/create",
                        form: true,
                        body: task
                    })
                })
            })
        })
    })

    it("Test nothing yet", () => {
        expect(true).to.equal(true)
    })

    after(function () {
        // Delete user, and its task
        cy.request({
            method: "DELETE",
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})