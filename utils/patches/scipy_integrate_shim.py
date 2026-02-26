class MockIntegrate:
    def odeint(self, *args, **kwargs): return [0]
    def solve_ivp(self, *args, **kwargs): 
        class Result: y = [0]; t = [0]; success = True
        return Result()
integrate = MockIntegrate()
