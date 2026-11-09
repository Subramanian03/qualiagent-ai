function Topbar({
  currentPage,
  selectedProject
}) {
  function getTitle() {
    if (currentPage === "dashboard") {
      return "Dashboard";
    }

    if (currentPage === "projects") {
      return "Projects";
    }

    if (currentPage === "workspace") {
      return selectedProject
        ? selectedProject.name
        : "Project Workspace";
    }

    if (currentPage === "test-cases") {
      return "Test Case Workspace";
    }

    if (currentPage === "automation") {
      return "Automation Workspace";
    }

    if (currentPage === "executions") {
  return "Executions Workspace";
}

    if (currentPage === "scenarios") {
  return "Test Scenarios";
}

    if (currentPage === "reports") {
  return "Reports Workspace";
}

    if (currentPage === "requirements") {
  return "Requirements";
}

    return "QualiAgent";
  }


  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">
          AI QUALITY ENGINEERING PLATFORM
        </p>

        <h2>{getTitle()}</h2>
      </div>
    </header>
  );
}


export default Topbar;