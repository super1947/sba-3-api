import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Seoul_CCTV_Plan import SeoulCCTV

if __name__ == "__main__":
    CCTV = SeoulCCTV()
    