import time

class TestCase():
    __slots__=["func","args_","kwargs","expected_return","iteration", "status", "results"]
    """
    func: the function that is going to be tested
    args: tuple of arguments
    kwargs: ditc of keyword arguments
    expected_return: an object that is expected as return
    iteration: int, the number of excution time to measure average execution time
    status: None: test is ready to run, Ture: the result was correct, Flase: unexpected return was given
    results: dict{"actual_return", "average_execution_time"}
    """
    
    def __init__(self, func, args_, kwargs, expected_return, iteration):
        self.func=func
        self.args_=args_
        self.kwargs=kwargs
        self.expected_return=expected_return 
        self.iteration=iteration
        self.status=None
        self.results={"actual_return":None, "average_execution_time":None,}
        
    def run(self):
        all_successful=True
        total_execution_time=0
        for i in range(self.iteration):
            t0=time.time()
            actual_return=self.func(*self.args_, **self.kwargs)
            t1=time.time()
            total_execution_time+=t1-t0
            if actual_return!=self.expected_return:
                all_successful=False
        self.status=all_successful
        self.results["actual_return"]=actual_return
        self.results["average_execution_time"]=total_execution_time/self.iteration


class SimpleUnitTester():
    __slots__=["cases_","func"]
    """
    func: the function that is going to be tested. referencial transparency of the fucntion is anticipated.
    cases_: list of TestCase obj
    """
    
    def __init__(self,func):
        self.func=func
        self.cases_=[]
        
    def add_new_case(self, args_=[],kwargs={},expected_return=None,iteration=1):
        self.cases_.append(TestCase(func=self.func, args_=args_, kwargs=kwargs, expected_return=expected_return, iteration=iteration))
    
    def add_new_cases(self, formated_cases_):
        for formated_case in formated_cases_:
            args_=()
            kwargs={}
            expected_return=formated_case[-1]
            if len(formated_case)==3:
                args_=formated_case[0]
                kwargs=formated_case[1]
            else:
                if isinstance(formated_case[0], tuple):
                    args_=formated_case[0]
                else:
                    kwargs=formated_case[0]
            self.cases_.append(TestCase(func=self.func, args_=args_, kwargs=kwargs, expected_return=expected_return, iteration=1))
    
    def run_test(self):
        func_name=repr(self.func).split()[1]
        print(f"Test for function {func_name}")
        for i,case in enumerate(self.cases_):
            case.run()
            if case.status:
                print(f"  Case{i+1}: Successful in {case.results['average_execution_time']}s | {case.args_} {case.kwargs} => {case.expected_return}")
            else:
                print(f"  Case{i+1}: Failed in {case.results['average_execution_time']}s | {case.args_} {case.kwargs} => {case.expected_return}\n    The expected return was {case.expected_return} but {case.results['actual_return']} was returned in reality.")