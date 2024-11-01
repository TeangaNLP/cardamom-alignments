from wasmer import engine, Store, Module, Instance
from . import align

store = Store()

# Let's compile the module to be able to execute it!
module = Module(store, """
(module
  (type (func (param i32 i32) (result i32)))
  (func (export "sum") (type 0) (param i32) (param i32) (result i32)
    local.get 0
    local.get 1
    i32.add))
""")

# Now the module is compiled, we can instantiate it.
instance = Instance(module)

# Call the exported `sum` function.
result = instance.exports.sum(5, 37)

print(result) # 42!
