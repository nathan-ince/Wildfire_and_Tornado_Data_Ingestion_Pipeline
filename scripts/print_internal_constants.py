def main():
  for name in (
    "__annotations__",
    "__builtins__",
    "__cached__",
    "__dict__",
    "__doc__",
    "__file__",
    "__loader__",
    "__name__",
    "__package__",
    "__path__",
    "__spec__"
  ):
    print(f"n = {name}")
    print(f"r = {globals().get(name)!r}")
    print(f"s = {globals().get(name)!s}")
    print(f"a = {globals().get(name)!a}")
    print("\n")

if __name__ == "__main__":
  main()
