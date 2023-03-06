import projects from '../../../../fixtures/projects/projects.json'

const currentProject = projects[1];

describe('I can create a recommandation with no resource as a switcthender', () => {
    beforeEach(() => {
        cy.login("jeanne");
    })

    it('creates a reco', () => {

        cy.visit('/projects')

        cy.contains(currentProject.fields.name).click({force:true});
        cy.contains('Conseiller le projet').click({force:true});

        cy.contains("Recommandations").click({ force: true })

        cy.url().should('include', '/actions')

        cy.contains("Ajouter une recommandation").click({ force: true })

        cy.get("#push-noresource").click({ force: true });

        const now = new Date();

        cy.get('#intent')
            .type('fake recommandation with no resource', { force: true })
            .should('have.value', 'fake recommandation with no resource')

        cy.get('textarea')
            .type(`fake recommandation content with no resource : ${now}`, { force: true })
            .should('have.value', `fake recommandation content with no resource : ${now}`)

        cy.get("[type=submit]").click({ force: true });

        cy.url().should('include', '/actions')
    })
})
