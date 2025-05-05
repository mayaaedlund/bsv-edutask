describe("Test CRUD of todo item", () => {
    let userObj
    let taskObj

    before(function () {
        // Add user
        cy.createUser().then(user => userObj = user)
    })

    beforeEach(function () {
        // Delete task if previously created
        if (taskObj) {
            cy.deleteTask(taskObj.id)
        }

        // Add task and assign to user
        cy.createTask(userObj.id).then((task) => {
            taskObj = task

            // Login user, and navigate to detail view of task
            cy.navigateToDetailView(userObj, taskObj)
        })
    })

    it("TC 2.1 - Toggle to 'done'", () => {
        cy.contains(taskObj.todos).as("todoDescription").prev().as("toggleIcon")
        cy.get("@todoDescription").should("not.have.css", "text-decoration-line", "line-through")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("have.css", "text-decoration-line", "line-through")
    })

    it("TC 2.2 - Toggle to 'active'", () => {
        // Set todo to 'done' through backend
        cy.setTodoDone(taskObj, true)

        // Refresh by navigating to detail view again
        cy.navigateToDetailView(userObj, taskObj)

        cy.contains(taskObj.todos).as("todoDescription").prev().as("toggleIcon")
        cy.get("@todoDescription").should("have.css", "text-decoration-line", "line-through")
        cy.get("@toggleIcon").click()
        cy.get("@todoDescription").should("not.have.css", "text-decoration-line", "line-through")
    })

    // Fails because TaskDetail does not wait for todo to update done status, but it works when trying manually in browser
    it("TC 3.1 - Delete todo item", () => {
        cy.contains(taskObj.todos).as("todoDescription").next().as("deleteBtn")
        cy.get("@deleteBtn").click()
        cy.get("@todoDescription").should("not.exist")   // fails, the todo is still there

        // This works though. cy.wait() does not solve it
        // cy.navigateToDetailView(userObj, taskObj)
        // cy.contains(taskObj.todos).should("not.exist")
    })

    after(function () {
        // Delete user and related tasks etc
        cy.deleteUser(userObj)
    })
})
