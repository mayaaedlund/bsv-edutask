// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

// Create a user from fixture and return the user
Cypress.Commands.add("createUser", (fixture="user.json") => {
    cy.fixture(fixture).then((user) => {
        cy.request({
            method: "POST",
            url: "http://localhost:5000/users/create",
            form: true,
            body: user
        }).then((response) => {
            return {...user, id: response.body._id.$oid}
        })
    })
})

// Delete user and related tasks
Cypress.Commands.add("deleteUser", (user) => {
    cy.request({
        method: "DELETE",
        url: `http://localhost:5000/users/${user.id}`
    })
})

// Create a task for user, and return the task
Cypress.Commands.add("createTask", (userId, fixture="task.json") => {
    cy.fixture(fixture).then((task) => {
        let taskObj = {...task, userid: userId}

        cy.request({
            method: "POST",
            url: "http://localhost:5000/tasks/create",
            form: true,
            body: taskObj
        }).then((response) => {
            console.log("Response from create task:", response)

            // Find the recently added task by title, and get the task id and todo id
            const createdTask = response.body.find(t => t.title === taskObj.title)
            taskObj.id = createdTask._id.$oid
            taskObj.todoId = createdTask.todos[0]._id.$oid
            return taskObj
        })
    })
})

// Delete a task by id
Cypress.Commands.add("deleteTask", (taskId) => {
    cy.request({
        method: "DELETE",
        url: `http://localhost:5000/tasks/byid/${taskId}`,
    })
})

// Login user, and navigate to detail view of task
Cypress.Commands.add("navigateToDetailView", (user, task) => {
    cy.visit("/")                            // home page
    cy.get("form").within(() => {
        cy.get("#email").type(user.email)    // enter email
        cy.contains("Login").click()         // login
    })
    cy.contains(task.title).click()          // open detail view
})

// Update todo item with done = true (toggle to done)
Cypress.Commands.add("setTodoDone", (task, done) => {
    const todoData = `data={'$set': {'done': ${done}}}`
    cy.request({
        method: "PUT",
        url: `http://localhost:5000/todos/byid/${task.todoId}`,
        body: todoData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache'
        }
    })
})
