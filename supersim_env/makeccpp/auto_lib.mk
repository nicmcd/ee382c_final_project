# Copyright (c) 2014, Nic McDonald
# All rights reserved.
#
# license available at https://raw.github.com/nicmcd/make-c-cpp/master/LICENSE
#
# THIS FILE SHOULD NOT BE ALTERED !!!

.SUFFIXES:

TGT_DLIB := $(BINARY_BASE)/lib$(PROGRAM_NAME).so
TGT_SLIB := $(BUILD_BASE)/lib$(PROGRAM_NAME).a
TST_APP := $(BINARY_BASE)/$(PROGRAM_NAME)$(TEST_SUFFIX)

HDR_INC := -I$(SOURCE_BASE) $(patsubst %,-I%,$(HEADER_DIRS))

ALL_SRCS := $(foreach EXT,$(SRC_EXTS),$(shell find $(SOURCE_BASE) -type f -iname "*$(EXT)"))
ALL_HDRS := $(foreach EXT,$(HDR_EXTS),$(shell find $(SOURCE_BASE) -type f -iname "*$(EXT)"))
ALL_DEPS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.d,$(ALL_SRCS))
ALL_OBJS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.o,$(ALL_SRCS))

TST_UNIT_SRCS := $(foreach EXT,$(SRC_EXTS),$(shell find $(SOURCE_BASE) -type f -iname "*$(TEST_SUFFIX)$(EXT)"))
TST_UNIT_HDRS := $(foreach EXT,$(HDR_EXTS),$(shell find $(SOURCE_BASE) -type f -iname "*$(TEST_SUFFIX)$(EXT)"))
TST_UNIT_DEPS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.d,$(TST_UNIT_SRCS))
TST_UNIT_OBJS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.o,$(TST_UNIT_SRCS))

TGT_SRCS := $(filter-out $(TST_UNIT_SRCS),$(ALL_SRCS))
TGT_HDRS := $(filter-out $(TST_UNIT_HDRS),$(ALL_HDRS))
TGT_DEPS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.d,$(TGT_SRCS))
TGT_OBJS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.o,$(TGT_SRCS))

LIB_HDRS := $(patsubst $(SOURCE_BASE)%,$(INCLUDE_BASE)%,$(TGT_HDRS))

TST_DEPS_SRCS := $(TGT_SRCS)
TST_DEPS_DEPS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.d,$(TST_DEPS_SRCS))
TST_DEPS_OBJS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%.o,$(TST_DEPS_SRCS))

SRC_DIRS := $(shell find $(SOURCE_BASE) -type d -print)
BLD_DIRS := $(patsubst $(SOURCE_BASE)%,$(BUILD_BASE)%,$(SRC_DIRS))
LIB_DIRS := $(patsubst $(SOURCE_BASE)%,$(INCLUDE_BASE)%,$(SRC_DIRS))

ALL_EXTS := $(shell echo $(SRC_EXTS) $(HDR_EXTS) | tr " " , | tr -d .)
LINT_FLAGS += --root=$(SOURCE_BASE) --extensions=$(ALL_EXTS)
LINT_OUT := $(BUILD_BASE)/$(PROGRAM_NAME).lint

GTEST_MAIN := $(GTEST_BASE)/make/gtest_main.a

VERBOSE = 0
ifeq ($(VERBOSE), 0)
  AT=@
else
  AT=
endif

.PHONY: all lint libd libs libh test clean count updatemk check

all: lint libd libs libh test

libd: $(TGT_DLIB)

libs: $(TGT_SLIB)

libh: $(LIB_HDRS)

lint: $(LINT_OUT)

test: $(TST_APP)

$(BINARY_BASE):
	$(AT)mkdir -p $@

$(BLD_DIRS):
	$(AT)mkdir -p $@

$(LIB_DIRS):
	$(AT)mkdir -p $@

$(LIB_HDRS): $(INCLUDE_BASE)/%: $(SOURCE_BASE)/% | $(LIB_DIRS)
	@echo [INC] $<
	$(AT)cp $< $@

$(LINT_OUT): $(ALL_SRCS) $(ALL_HDRS) | $(BUILD_BASE)
ifneq ($(wildcard $(LINT)),)
	@echo [LINT]
	$(AT)python $(LINT) $(LINT_FLAGS) $(ALL_SRCS) $(ALL_HDRS)
	$(AT)echo "linted" > $(LINT_OUT)
else
	@echo -n
endif

$(TGT_DLIB): $(TGT_SLIB) | $(BINARY_BASE)
	@echo [LD] $@
	$(AT)$(CXX) $(CXX_FLAGS) -shared -Wl,-soname,$@ -o $@ $< $(LINK_FLAGS)

$(TGT_SLIB): $(TGT_OBJS) | $(BUILD_BASE)
	@echo [AR] $@
	$(AT)$(AR) rcs $@ $(TGT_OBJS)

$(TGT_OBJS): $(BUILD_BASE)/%.o: $(SOURCE_BASE)/% | $(BLD_DIRS)
	@echo [CC] $<
	$(AT)$(CXX) $(CXX_FLAGS) -fPIC $(HDR_INC) -MD -MP -c -o $@ $<

$(TST_APP): $(TST_UNIT_OBJS) $(TGT_SLIB) $(STATIC_LIBS) | $(BINARY_BASE)
ifneq ($(wildcard $(GTEST_MAIN)),)
	@echo [LD] $@
	$(AT)$(CXX) $(CXX_FLAGS) $(TST_UNIT_OBJS) $(TGT_SLIB) $(STATIC_LIBS) $(GTEST_MAIN) $(LINK_FLAGS) -o $(TST_APP) -lpthread
else
	@echo -n
endif

$(TST_UNIT_OBJS): $(BUILD_BASE)/%.o: $(SOURCE_BASE)/% | $(BLD_DIRS)
ifneq ($(wildcard $(GTEST_MAIN)),)
	@echo [CC] $<
	$(AT)$(CXX) $(CXX_FLAGS) $(HDR_INC) -I$(GTEST_BASE)/include -MD -MP -c -o $@ $<
else
	@echo -n
endif

check: test
ifneq ($(wildcard $(GTEST_MAIN)),)
	@$(TST_APP)
else
	@echo -n
endif

clean:
ifeq ($(SOURCE_BASE), $(BUILD_BASE))
	@echo "Awwww, clean will destroy your source if you build in the same spot!"
	false
endif
ifeq ($(SOURCE_BASE), $(BINARY_BASE))
	@echo "Awwww, clean will destroy your source if you build in the same spot!"
	false
endif
ifeq ($(SOURCE_BASE), $(INCLUDE_BASE))
	@echo "Awwww, clean will destroy your source if you build in the same spot!"
	false
endif
	$(AT)rm -rf $(BUILD_BASE) $(BINARY_BASE) $(INCLUDE_BASE)

count:
	@echo "lines words bytes file"
	@wc $(ALL_SRCS) $(ALL_HDRS) | sort -n -k1
	@echo "files : "$(shell echo $(ALL_SRCS) $(ALL_HDRS) | wc -w)
	@echo "commits : "$(shell git rev-list HEAD --count)

-include $(ALL_DEPS)
