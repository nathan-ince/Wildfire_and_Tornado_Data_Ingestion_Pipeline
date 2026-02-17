# **Logging**

This note contains information about logging in our project.

---

### **Configure Logging**

In constrast to a long-running application, where you would typically configure logging in one place near the entry point of the application...

This project is not long-running. It contains some scripts that can be called.

With that in mind, we configure logging at the entry point of each script.

---

### **Structured Logging**

We decided to go with structured logging.

As opposed unstructured logging, where each log is a plain text message with no definite structure, structured logging is method of logging where each log is structured in a key-value format, like JSON.

Structured logging is intended to be machine readable, making it easier to search and filter though. This makes structured logging more scalable and better suited for production-grade systems.

---
