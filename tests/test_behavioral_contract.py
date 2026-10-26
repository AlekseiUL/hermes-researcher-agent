import copy, importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('benchmark_grade',ROOT/'evals/regression-v1/grade.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class Benchmark(unittest.TestCase):
    def test_golden_and_adversarial_outputs(self):
        cases=json.loads((ROOT/'evals/regression-v1/cases.json').read_text())
        for case in cases:
            with self.subTest(case=case['id']):
                good=case['golden_annotation']; self.assertEqual(m.grade(case,good),[])
                for malformed in [None, [], 'invalid', 42]:
                    bad=copy.deepcopy(good); bad['sections']=malformed
                    self.assertTrue(m.grade(case,bad))
                bad=copy.deepcopy(good); bad['claims'].append({'fact':'invented benefit','source':'https://invalid.invalid/invented'})
                self.assertTrue(m.grade(case,bad))
                bad=copy.deepcopy(good); del bad['sections'][case['required_sections'][0]]
                self.assertTrue(m.grade(case,bad))
                bad=copy.deepcopy(good); bad['limitations']=[]
                self.assertTrue(m.grade(case,bad))
if __name__=='__main__': unittest.main()
