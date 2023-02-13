describe('I can follow a project', () => {

    beforeEach(() => {
        cy.login("bob");
    })

    it('goes to the homepage and create a project with the main CTA', () => {

        cy.visit('/')

        cy.get('a').should('have.class', 'fr-btn fr-text--xl custom-button').contains('Solliciter UrbanVitaliz').click({ force: true })

        cy.url().should('include', '/onboarding/')

        cy.get('#id_name')
            .type('fake project name', { force: true })
            .should('have.value', 'fake project name')

        cy.get('#input-project-address')
            .type('143 rue fake', { force: true })
            .should('have.value', '143 rue fake')

        cy.get('[name=postcode]')
            .type('42424', { force: true })
            .should('have.value', '42424')

        cy.get('#input-project-description')
            .type('Fake project description', { force: true })
            .should('have.value', 'Fake project description')

        cy.get('#id_response_1')
            .type('Fake project description precision', { force: true })
            .should('have.value', 'Fake project description precision')

        cy.get('#id_response_2_0')
            .check({ force: true })

        cy.document().then((doc) => {
            var iframe = doc.getElementById('id_captcha').querySelector('iframe');
            var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
            innerDoc.querySelector('.recaptcha-checkbox').click()
        })

        cy.wait(500)

        cy.contains('Envoyer ma demande').click({ force: true });

        // cy.url().should('include', '/projects/survey/')

        // cy.get(".introjs-skipbutton").click({ force: true });

        // cy.contains('fake project name').click({ force: true });
    })
})
