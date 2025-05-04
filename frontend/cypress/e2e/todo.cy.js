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

    it("TC 2.1 - Toggle done", () => {
        cy.contains(taskObj.todos).as("todoDescription")
        cy.get("@todoDescription").prev().as("toggleIcon")
        // cy.get("@todoDescription").text().should("not.be.")
        // cy.get("@toggleIcon").should()
    })

    it("TC 1.1.1 - 'Add' button is disabled when input is empty", () => {
        cy.get("input[placeholder='Add a new todo item']").clear()
        cy.get("form.inline-form input[type='submit']").should("be.disabled")
    })

    it("TC 1.2.1 - System does not add todo when input is empty", () => {
        cy.get(".todo-list .todo-item").then(($itemsBefore) => {
            const initialCount = $itemsBefore.length;
    
            cy.get("input[placeholder='Add a new todo item']").clear({ force: true });
            cy.get("form.inline-form input[type='submit']").click({ force: true });
    
            cy.get(".todo-list .todo-item").should("have.length.at.most", initialCount);
        });
    });

    it("TC 1.1.2 & 1.2.2 - System adds todo when input is not empty", () => {
        const todoText = "Test todo item"
        cy.get("input[placeholder='Add a new todo item']").clear({ force: true }).type(todoText, { force: true })
        cy.get("form.inline-form input[type='submit']").click({ force: true })
        cy.get(".todo-list .todo-item").last().should("contain.text", todoText)
    })

    after(function () {
        // Delete user and assigned task
        cy.request({
            method: "DELETE",
            url: `http://localhost:5000/users/${userObj.id}`
        })
    })
})