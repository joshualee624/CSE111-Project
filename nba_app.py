import sys
from python.NBAApp import NBAApp

def main():
   
    try:
        app = NBAApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

