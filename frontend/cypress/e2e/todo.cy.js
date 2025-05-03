describe("Test CRUD of todo item", () => {
    let userObj
    let taskObj

    before(function () {
        // Add user
        cy.fixture("user.json").then((user) => {
            cy.request({
                method: "POST",
                url: "http://localhost:5000/users/create",
                form: true,
                body: user
            }).then((response) => {
                userObj = {...user, id: response.body._id.$oid}
            })
        })
    })

    beforeEach(function () {
        // Delete task if created
        if (taskObj) {
            cy.request({
                method: "DELETE",
                url: `http://localhost:5000/tasks/byid/${taskObj.id}`,
            })
        }

        // Add task and assign to user
        cy.fixture("task.json").then((task) => {
            taskObj = {...task, userid: userObj.id}

            cy.request({
                method: "POST",
                url: "http://localhost:5000/tasks/create",
                form: true,
                body: taskObj
            }).then((response) => {
                // Find the recently added task by title, and get the id
                taskObj.id = response.body.find(t => t.title === taskObj.title)._id.$oid

                // Navigate to detail view of task
                cy.visit("/")                               // home page
                cy.get("form").within(() => {
                    cy.get("#email").type(userObj.email)    // enter email
                    cy.contains("Login").click()            // login
                })
                cy.get("a").contains(taskObj.title).click() // open detail view
            })
        })
    })

    it("TC 2.1 - Toggle to 'done'", () => {
        cy.contains(taskObj.todos).as("todoDescription").prev().as("toggleIcon")
        cy.get("@todoDescription").should("not.have.css", "text-decoration-line", "line-through")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("have.css", "text-decoration-line", "line-through")
    })

    it("TC 2.2 - Toggle to 'active'", () => {
        cy.contains(taskObj.todos).as("todoDescription").prev().as("toggleIcon")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("have.css", "text-decoration-line", "line-through")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("not.have.css", "text-decoration-line", "line-through")
    })

    it("TC 2.1 & 2.2 - Toggle 'done' and 'active'", () => {
        cy.contains(taskObj.todos).as("todoDescription").prev().as("toggleIcon")
        cy.get("@todoDescription").should("not.have.css", "text-decoration-line", "line-through")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("have.css", "text-decoration-line", "line-through")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("not.have.css", "text-decoration-line", "line-through")
    })

    after(function () {
        // Delete user and assigned task
        cy.request({
            method: "DELETE",
            url: `http://localhost:5000/users/${userObj.id}`
        })
    })
})
