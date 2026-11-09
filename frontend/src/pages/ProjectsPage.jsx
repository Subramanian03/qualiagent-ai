function ProjectsPage({
  projects,
  onCreateProject,
  onOpenProject
}) {
  return (
    <section className="projects-page">
      <div className="page-intro">
        <div>
          <span className="section-label">
            QA WORKSPACES
          </span>

          <h3>Projects</h3>

          <p>
            Manage the applications and QA
            workspaces being tested through QualiAgent.
          </p>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={onCreateProject}
        >
          + New Project
        </button>
      </div>


      {projects.length === 0 ? (
        <div className="empty-state">
          <h4>No projects yet</h4>

          <p>
            Create your first QA project to begin.
          </p>
        </div>
      ) : (
        <div className="project-list">
          {projects.map((project) => (
            <article
              className="project-list-card"
              key={project.id}
              onClick={() =>
                onOpenProject(project)
              }
              role="button"
              tabIndex={0}
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" ||
                  event.key === " "
                ) {
                  event.preventDefault();
                  onOpenProject(project);
                }
              }}
            >
              <div className="project-list-icon">
                {project.name
                  .slice(0, 2)
                  .toUpperCase()}
              </div>

              <div className="project-list-info">
                <div className="project-list-title">
                  <h4>{project.name}</h4>

                  <span>
                    {project.application_type
                      .toUpperCase()}
                  </span>
                </div>

                <p>{project.description}</p>

                <small>
                  Project ID: {project.id}
                </small>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}


export default ProjectsPage;