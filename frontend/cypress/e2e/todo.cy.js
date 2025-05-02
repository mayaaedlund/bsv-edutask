describe("Test CRUD of todo item", () => {
    let uid
    let tid

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
            })
        })
    })

    beforeEach(function () {
        // Delete task if created
        if (tid) {
            cy.request({
                method: "DELETE",
                url: `http://localhost:5000/tasks/byid/${tid}`,
            })
        }

        // Add a fresh task for user (in same manner as in TaskCreator.js)
        cy.fixture("task.json").then((task) => {
            task.userid = uid

            cy.request({
                method: "POST",
                url: "http://localhost:5000/tasks/create",
                form: true,
                body: task
            }).then((res) => {
                const inserted_task = res.body.find(t => t.title === task.title)
                tid = inserted_task._id.$oid
            })
        })
    })

    it("Test nothing yet", () => {
        expect(true).to.equal(true)
    })

    it("Test nothing yet2", () => {
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