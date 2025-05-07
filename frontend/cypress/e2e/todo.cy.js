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

    it("TC 1.1.1 - 'Add' button is disabled when input is empty", () => {
        cy.get("input[placeholder='Add a new todo item']").clear()
        cy.get("form.inline-form input[type='submit']").should("be.disabled")
    })

    it("TC 1.1.2 - 'Add' button is enabled when input is not empty", () => {
        const todoText = "Test todo item"
        cy.get("input[placeholder='Add a new todo item']").clear().type(todoText)
        cy.get("form.inline-form input[type='submit']").should("not.be.disabled")
    })
    

    it("TC 1.2.1 - System does not add todo when input is empty", () => {
        cy.get(".todo-list .todo-item").then(($itemsBefore) => {
            const initialCount = $itemsBefore.length;
    
            cy.get("input[placeholder='Add a new todo item']").clear({ force: true });
            cy.get("form.inline-form input[type='submit']").click({ force: true });

            cy.wait(500);
    
            cy.get(".todo-list .todo-item").should("have.length.at.most", initialCount);
        });
    });

    it("TC 1.2.2 - System adds todo when input is not empty", () => {
        const todoText = "Test todo item"

        cy.get("input[placeholder='Add a new todo item']").clear({ force: true }).type(todoText, { force: true })
        cy.get("form.inline-form input[type='submit']").click({ force: true });
        cy.get(".todo-list .todo-item").last().should("contain.text", todoText)
    })
    

    after(function () {
        // Delete user and related tasks etc
        cy.deleteUser(userObj)
    })
})